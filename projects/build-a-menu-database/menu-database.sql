--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: build_menu; Type: SCHEMA; Schema: -; Owner: khoatran
--

CREATE SCHEMA build_menu;


ALTER SCHEMA build_menu OWNER TO khoatran;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: address; Type: TABLE; Schema: build_menu; Owner: khoatran
--

CREATE TABLE build_menu.address (
    id integer NOT NULL,
    street_number character varying(10),
    street_name character varying(20),
    city character varying(20),
    state character varying(15),
    google_map_link character varying(50),
    restaurant_id integer
);


ALTER TABLE build_menu.address OWNER TO khoatran;

--
-- Name: categories_dishes; Type: TABLE; Schema: build_menu; Owner: khoatran
--

CREATE TABLE build_menu.categories_dishes (
    category_id character(2) NOT NULL,
    dish_id integer NOT NULL,
    price money
);


ALTER TABLE build_menu.categories_dishes OWNER TO khoatran;

--
-- Name: category; Type: TABLE; Schema: build_menu; Owner: khoatran
--

CREATE TABLE build_menu.category (
    id character(2) NOT NULL,
    name character varying(20),
    description character varying(200)
);


ALTER TABLE build_menu.category OWNER TO khoatran;

--
-- Name: dish; Type: TABLE; Schema: build_menu; Owner: khoatran
--

CREATE TABLE build_menu.dish (
    id integer NOT NULL,
    name character varying(50),
    description character varying(200),
    hot_and_spicy boolean
);


ALTER TABLE build_menu.dish OWNER TO khoatran;

--
-- Name: restaurant; Type: TABLE; Schema: build_menu; Owner: khoatran
--

CREATE TABLE build_menu.restaurant (
    id integer NOT NULL,
    name character varying(20),
    description character varying(100),
    rating numeric,
    telephone character(10),
    hours character varying(100)
);


ALTER TABLE build_menu.restaurant OWNER TO khoatran;

--
-- Name: review; Type: TABLE; Schema: build_menu; Owner: khoatran
--

CREATE TABLE build_menu.review (
    id integer NOT NULL,
    rating numeric,
    description character varying(100),
    date date,
    restaurant_id integer
);


ALTER TABLE build_menu.review OWNER TO khoatran;

--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);


--
-- Name: address address_restaurant_id_key; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.address
    ADD CONSTRAINT address_restaurant_id_key UNIQUE (restaurant_id);


--
-- Name: categories_dishes categories_dishes_pkey; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.categories_dishes
    ADD CONSTRAINT categories_dishes_pkey PRIMARY KEY (category_id, dish_id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: dish dish_pkey; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.dish
    ADD CONSTRAINT dish_pkey PRIMARY KEY (id);


--
-- Name: restaurant restaurant_pkey; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.restaurant
    ADD CONSTRAINT restaurant_pkey PRIMARY KEY (id);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);


--
-- Name: address address_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.address
    ADD CONSTRAINT address_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES build_menu.restaurant(id);


--
-- Name: categories_dishes categories_dishes_category_id_fkey; Type: FK CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.categories_dishes
    ADD CONSTRAINT categories_dishes_category_id_fkey FOREIGN KEY (category_id) REFERENCES build_menu.category(id);


--
-- Name: categories_dishes categories_dishes_dish_id_fkey; Type: FK CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.categories_dishes
    ADD CONSTRAINT categories_dishes_dish_id_fkey FOREIGN KEY (dish_id) REFERENCES build_menu.dish(id);


--
-- Name: review review_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: build_menu; Owner: khoatran
--

ALTER TABLE ONLY build_menu.review
    ADD CONSTRAINT review_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES build_menu.restaurant(id);


--
-- PostgreSQL database dump complete
--

