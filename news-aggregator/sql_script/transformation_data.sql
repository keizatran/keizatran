DROP TABLE IF EXISTS `first-hold-417112.marts.data_post`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.data_post` AS 

SELECT DISTINCT
  GENERATE_UUID() id
  , post_id
  , publisher_name
  , date_published
  , date_modified
FROM `first-hold-417112.marts.post_unified_data`;

DROP TABLE IF EXISTS `first-hold-417112.marts.data_post_content`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.data_post_content` AS 

SELECT DISTINCT 
  GENERATE_UUID() id
  , post_id 
  , post_title
  , post_subtitle
  , post_description
  , post_content
  , post_link
  , NULL keyword
  , NULL word_count
  , NULL comment_count
FROM `first-hold-417112.marts.post_unified_data`;

-- SELECT post_id, schema_data, json_extract(schema_data, '$.wordCount') as type
-- FROM (
-- SELECT *, JSON_EXTRACT_ARRAY(REGEXP_REPLACE(schema_graph, '@', '')) AS t
-- FROM `first-hold-417112.firsttable01.sample_table`
-- ), UNNEST (t) as schema_data

DROP TABLE IF EXISTS `first-hold-417112.marts.data_author`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.data_author` AS 

SELECT DISTINCT 
  GENERATE_UUID() id
  , post_id
  , author_id
  , author_name
FROM `first-hold-417112.marts.post_unified_data`;




DROP TABLE IF EXISTS `first-hold-417112.marts.data_publisher`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.data_publisher` AS 

SELECT DISTINCT 
  GENERATE_UUID() id
  , post_id
  , publisher_name
  , NULL publisher_link
FROM `first-hold-417112.marts.post_unified_data`;


DROP TABLE IF EXISTS `first-hold-417112.marts.data_category`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.data_category` AS 

SELECT DISTINCT 
  GENERATE_UUID() id
  , post_id
  , NULL category_id
  , post_category
FROM `first-hold-417112.marts.post_unified_data`;



DROP TABLE IF EXISTS `first-hold-417112.marts.data_media`; 
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.data_media` AS 

SELECT DISTINCT 
  GENERATE_UUID() id
  , post_id
  , image_url
  , video_url
FROM `first-hold-417112.marts.post_unified_data`;

