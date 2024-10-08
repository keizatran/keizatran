DROP TABLE IF EXISTS `first-hold-417112.master_data.dwh_fact_tbl_news`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.dwh_fact_tbl_news` AS 

SELECT DISTINCT
    p.post_id
  , p.date_published
  , p.date_modified
  , pl.publisher_name
  , a.author_name
  , pc.post_title
  , pc.post_content
  , pc.post_link
FROM `first-hold-417112.marts.data_post` p 
LEFT JOIN `first-hold-417112.marts.data_post_content` pc
  ON p.post_id = pc.post_id
LEFT JOIN `first-hold-417112.marts.data_publisher` pl
  ON p.post_id = pl.post_id
LEFT JOIN `first-hold-417112.marts.data_media` m
  ON p.post_id = m.post_id
LEFT JOIN `first-hold-417112.marts.data_author` a
  ON p.post_id = a.post_id
LEFT JOIN `first-hold-417112.marts.data_category` c
  ON p.post_id = c.post_id
WHERE TRUE;
  -- AND CAST(p.date_published AS DATE) >= CURRENT_DATE() - INTERVAL 7 DAYS
