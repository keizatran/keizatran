DROP TABLE IF EXISTS `first-hold-417112.marts.post_unified_data`;
CREATE TABLE IF NOT EXISTS `first-hold-417112.marts.post_unified_data` AS 

WITH 
union_data AS (

  SELECT 
      post_id
    , post_title
    , NULL post_subtitle
    , post_description
    , post_content
    , post_link
    , category post_category
    , date_published
    , date_modified
    , publisher_name 
    , author_id
    , author_name
    , schema_graph
    , NULL media
  FROM `first-hold-417112.raw_data.raw__9to5google`

  UNION ALL

  SELECT 
      post_id
    , post_title
    , NULL post_subtitle
    , post_description
    , post_content
    , post_link
    , category post_category
    , date_published
    , date_modified
    , publisher_name 
    , author_id
    , author_name
    , schema_graph
    , NULL media
  FROM `first-hold-417112.raw_data.raw__9to5mac`

  UNION ALL

  SELECT 
      post_id
    , post_title
    , NULL post_subtitle
    , post_description
    , post_content
    , post_link
    , CAST(category AS STRING) post_category
    , date_published
    , date_modified
    , publisher_name 
    , author_id
    , author_name
    , schema_graph
    , NULL media
  FROM `first-hold-417112.raw_data.raw__techcrunch`

  UNION ALL

  SELECT  
      SAFE_CAST(id AS INT64) post_id
    , title post_title
    , sub_title post_subtitle
    , NULL post_description
    , body post_content
    , link post_link
    , NULL post_category
    , date_published
    , date_modified
    , publisher publisher_name
    , NULL author_id
    , author_name
    , NULL schema_graph
    , STRUCT(
        image_url
      , video_url
      , keyword
    ) AS media 
  FROM `first-hold-417112.raw_data.raw__engadget`

), transform_data AS (

  SELECT
      SAFE_CAST(post_id AS INT64) post_id
    , post_title
    , post_subtitle
    , post_description
    , post_content
    , post_link
    , post_category
    , SAFE_CAST(date_published AS TIMESTAMP) date_published
    , SAFE_CAST(date_modified AS TIMESTAMP) date_modified
    , publisher_name
    , author_id
    , author_name
    , schema_graph
    , media.image_url image_url
    , media.video_url video_url
    , media.keyword keyword
  FROM union_data 

), final AS (

  SELECT *
  FROM transform_data 

) 

SELECT *  
FROM final; 