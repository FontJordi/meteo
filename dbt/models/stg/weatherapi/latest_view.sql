    with ranked as (
        select *, 
        ROW_NUMBER() OVER (PARTITION BY name order by timedate desc)
        from {{ ref('convert_types') }} 
    ), final as (

        select 

        name,
        weather,
        temperature - 273.15 as temp,
        feels_like - 273.15 as feels_like,
        humidity,
        wind_speed,
        cloudiness,
        coord_lat,
        coord_lon,
        timedate

        from ranked
        where row_number = 1
        order by name
        )

select * from final