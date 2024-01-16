    with ranked as (
        select *, 
        ROW_NUMBER() OVER (PARTITION BY name order by dt desc)
        from {{ ref('dt_timestamp') }} 
    )
    select 

    name,
    weather_main,
    main_temp,
    main_feels_like,
    main_humidity,
    wind_speed,
    clouds_all,
    dt

    from ranked
    where row_number = 1
    order by name