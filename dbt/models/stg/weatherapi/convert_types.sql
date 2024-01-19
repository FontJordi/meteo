{{ config(materialized='table') }}
WITH source AS(
    
    SELECT *
    FROM {{ref("convert_nulls") }}
),

final AS (

    SELECT 

    coord_lon::NUMERIC,
    coord_lat::NUMERIC,
    weather_id::SMALLINT,
    weather,
    weather_description,
    weather_icon,
    base,
    temperature::NUMERIC(5,2),
    feels_like::NUMERIC(5,2),
    temp_min::NUMERIC(5,2),
    temp_max::NUMERIC(5,2),
    pressure::SMALLINT,
    humidity::SMALLINT,
    pressure_sea_level::SMALLINT,
    pressure_grnd_level::SMALLINT,
    visibility::SMALLINT,
    wind_speed::NUMERIC(5,2),
    wind_direction::SMALLINT,
    wind_gust::NUMERIC(5,2),
    cloudiness::SMALLINT,
    TO_TIMESTAMP(timedate::integer) as timedate,
    sys_type::SMALLINT,
    sys_id,
    country,
    TO_TIMESTAMP(sunrise::INTEGER) as sunrise,
    TO_TIMESTAMP(sunset::INTEGER) as sunset,
    timezone::SMALLINT,
    id::INTEGER,
    name,
    cod::SMALLINT,
    rain_1h::NUMERIC(5,2),
    rain_3h::NUMERIC(5,2),
    snow_1h::NUMERIC(5,2),
    snow_3h::NUMERIC(5,2),
    cast(insertdatetime as timestamp) as insertdatetime

    FROM source
    )

SELECT * FROM final