WITH final as (
    SELECT * FROM {{ ref('twoweeks') }}
) 

SELECT *
FROM final
WHERE DATE_PART('day', NOW()::timestamp - timedate::timestamp) > 14
