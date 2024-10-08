import os
import json
import html
import logging
import requests
import psycopg2
import psycopg2.extras
import lxml.html as lh
from uuid import uuid4, UUID
from pydantic import BaseModel, Field
from psycopg2.extensions import connection

##################################### search product #####################################


class Search_Products_SKU(BaseModel):
    slug: str


class Search_Products(BaseModel):
    sku: Search_Products_SKU


class Search_Products_Resp(BaseModel):
    data: list[Search_Products]
    total: int


def _search_products(page: int, limit: int):
    url = "https://thuocsi.vn/backend/marketplace/product/v2/search/fuzzy"
    token = os.getenv("THUOCSI_TOKEN")
    user_agent = os.getenv("THUOCSI_AGENT")
    data = {
        "offset": page * limit,
        "page": page + 1,
        "limit": limit,
        "getTotal": True,
        "text": None,
        "filter": {},
        "sort": "",
        "isAvailable": False,
        "searchStrategy": {"text": True, "keyword": True, "ingredient": True},
    }
    headers = {"Authorization": f"Bearer {token}", "User-Agent": f"{user_agent}"}

    try:
        cnn = requests.post(url=url, json=data, headers=headers)
        resp = Search_Products_Resp.parse_raw(cnn.text)
    except Exception as err:
        logging.error(f"[thuocsi][_search_products] has error: {err}")
        return
    else:
        return resp


def _update_search_products(resp: Search_Products_Resp):
    db_url = os.getenv("DWH")
    cnn = psycopg2.connect(db_url)
    cs = cnn.cursor()
    for data in resp.data:
        cs.execute(
            "insert into scrap.pharmacy_product_tracking (site, url) values (%s, %s)",
            ("thuocsi", f"https://thuocsi.vn/product/{data.sku.slug}"),
        )
    try:
        cnn.commit()
    except Exception as err:
        logging.error(f"[thuocsi][_search_products] has error: {err}")
        cnn.rollback()
    finally:
        cs.close()
        cnn.close()


def search_products(page: int = 0, limit: int = 30):
    try:
        while True:
            logging.info(f"[thuocsi][search_products] page {page} limit {limit}")

            resp = _search_products(page=page, limit=limit)

            if not resp:
                break

            _update_search_products(resp=resp)

            if (page + 1) * limit > resp.total:
                break

            page += 1

    except KeyboardInterrupt:
        pass

    logging.info(f"[thuocsi][search_products] exit")


##########################################################################################

#################################### get product raw #####################################


def _get_unraw_product_url(cnn: connection) -> list[str]:
    cs = cnn.cursor()
    cs.execute(
        "select url from scrap.pharmacy_product_tracking "
        "where raw_id is null and site = 'thuocsi'"
    )
    rs = cs.fetchall()
    cs.close()

    return [r[0] for r in rs]


def _get_product(url: str):
    token = os.getenv("THUOCSI_TOKEN")
    user_agent = os.getenv("THUOCSI_AGENT")
    headers = {"Authorization": f"Bearer {token}", "User-Agent": f"{user_agent}"}

    try:
        cnn = requests.get(url=url, headers=headers)
    except Exception as err:
        logging.error(f"[thuocsi][_get_product] has error: {err}")
        return
    else:
        return cnn.text


def _create_raw_product(cnn: connection, data: str):
    cs = cnn.cursor()
    new_uuid = uuid4()
    cs.execute(
        "insert into scrap.pharmacy_product_raw_data values (%s, %s)", (new_uuid, data)
    )
    cnn.commit()
    cs.close()
    return new_uuid


def _update_unraw_product(cnn: connection, url: str, new_uuid: UUID):
    cs = cnn.cursor()
    cs.execute(
        "update scrap.pharmacy_product_tracking set raw_id = %s where site = 'thuocsi' and url = %s",
        (new_uuid, url),
    )
    cnn.commit()
    cs.close()


def get_product():
    psycopg2.extras.register_uuid()

    db_url = os.getenv("DWH")
    cnn = psycopg2.connect(db_url)

    urls = _get_unraw_product_url(cnn=cnn)

    logging.info(f"[thuocsi][get_product] process {len(urls)} url")

    index = 0

    for url in urls:
        try:
            data = _get_product(url=url)

            if not data:
                continue

            new_uuid = _create_raw_product(cnn=cnn, data=data)
            _update_unraw_product(cnn=cnn, url=url, new_uuid=new_uuid)

        except Exception as err:
            logging.error(f"[thuocsi][get_product] has error: {err}")
            cnn.rollback()
        else:
            index += 1
            if index % 100 == 0:
                logging.info(f"[thuocsi][get_product] scrapped {index:5d} url")


##########################################################################################

################################### parse product raw ####################################


class Unparsed_Product(BaseModel):
    url: str
    raw_data: str


class Ingredient(BaseModel):
    ingredient_code: str = Field(alias="ingredientCode")
    volume: str | None


class Description(BaseModel):
    contraindication: str | None
    description: str | None
    dosage: str | None
    drug_interaction: str | None = Field(alias="drugInteraction")
    drug_overdose: str | None = Field(alias="drugOverdose")
    indication: str | None
    storage: str | None


class Product(BaseModel):
    image_urls: list[str] = Field(alias="imageUrls")
    sku: str
    ingredients: list[Ingredient]
    manufacturer_code: str = Field(alias="manufacturerCode")
    category_codes: list[str] = Field(alias="categoryCodes")
    name: str
    product_id: int = Field(alias="productId")
    unit: str
    origin: str
    volume: str
    weight: float
    description: Description


class Product_Props(BaseModel):
    product: Product


class Props(BaseModel):
    pageProps: Product_Props


class Full_Product(BaseModel):
    props: Props


def _get_unparsed_product(cnn: connection):
    cs = cnn.cursor()
    cs.execute(
        "select url, raw_data "
        "from scrap.pharmacy_product_tracking t "
        "left join scrap.pharmacy_product_raw_data r on t.raw_id = r.id "
        "where parsed_id is null and site = 'thuocsi' limit 1000"
    )
    rs = cs.fetchall()
    cs.close()
    return [Unparsed_Product(url=r[0], raw_data=r[1]) for r in rs]


def _update_product(product: Product, cnn: connection):
    cs = cnn.cursor()
    new_uuid = uuid4()
    cs.execute(
        "insert into scrap.pharmacy_thuocsi ("
        '   "id", product_id, sku, ingredients, manufacturer_code, category_codes,'
        "   name, origin, weight, description, contraindication, dosage,"
        "   drug_interaction, drug_overdose, indication, storage"
        ") values"
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            new_uuid,
            product.product_id,
            product.sku,
            json.dumps([dict(i) for i in product.ingredients]),
            product.manufacturer_code,
            json.dumps(product.category_codes),
            product.name,
            product.origin,
            product.weight,
            html.unescape(product.description.description or "").strip(),
            html.unescape(product.description.contraindication or "").strip(),
            html.unescape(product.description.dosage or "").strip(),
            html.unescape(product.description.drug_interaction or "").strip(),
            html.unescape(product.description.drug_overdose or "").strip(),
            html.unescape(product.description.indication or "").strip(),
            html.unescape(product.description.storage or "").strip(),
        ),
    )
    cnn.commit()
    cs.close()
    return new_uuid


def _update_parsed_product(cnn: connection, url: str, new_uuid: UUID):
    cs = cnn.cursor()
    cs.execute(
        "update scrap.pharmacy_product_tracking set parsed_id = %s where site = 'thuocsi' and url = %s",
        (new_uuid, url),
    )
    cnn.commit()
    cs.close()


def parse_product():
    psycopg2.extras.register_uuid()

    db_url = os.getenv("DWH")
    cnn = psycopg2.connect(db_url)

    unparsed_products = _get_unparsed_product(cnn=cnn)

    for unparsed_product in unparsed_products:
        try:
            body = lh.fromstring(unparsed_product.raw_data)
            data = body.xpath("//body/script")
            if not data:
                continue

            data = data[0].text
            parsed_product = Full_Product.parse_raw(data)
            product = parsed_product.props.pageProps.product
            new_uuid = _update_product(cnn=cnn, product=product)
            _update_parsed_product(cnn=cnn, url=unparsed_product.url, new_uuid=new_uuid)
        except Exception as err:
            logging.error(
                f"[thuocsi][parse_product] has error: {err}\n{unparsed_product.url}"
            )
            cnn.rollback()


##########################################################################################
