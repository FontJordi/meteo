{{ config(materialized='table') }}

SELECT *
FROM dt_timestamp
WHERE DATE_PART('day', NOW()::timestamp - dt::timestamp) < 14