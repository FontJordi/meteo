{{ config(materialized='table') }}
WITH source AS(
    
    SELECT *
    FROM {{ source ("weatherapi","meteo_insert")}}
    
), final AS(

SELECT 

    NULLIF(coord_lon, '') AS coord_lon,
    NULLIF(coord_lat, '') AS coord_lat,
    NULLIF(weather_id, '') AS weather_id,
    NULLIF(weather_main, '') AS weather,
    NULLIF(weather_description, '') AS weather_description,
    NULLIF(weather_icon, '') AS weather_icon,
    NULLIF(base, '') AS base,
    NULLIF(main_temp, '') AS temperature,
    NULLIF(main_feels_like, '') AS feels_like,
    NULLIF(main_temp_min, '') AS temp_min,
    NULLIF(main_temp_max, '') AS temp_max,
    NULLIF(main_pressure, '') AS pressure,
    NULLIF(main_humidity, '') AS humidity,
    NULLIF(main_sea_level, '') AS pressure_sea_level,
    NULLIF(main_grnd_level, '') AS pressure_grnd_level,
    NULLIF(visibility, '') AS visibility,
    NULLIF(wind_speed, '') AS wind_speed,
    NULLIF(wind_deg, '') AS wind_direction,
    NULLIF(wind_gust, '') AS wind_gust,
    NULLIF(clouds_all, '') AS cloudiness,
    NULLIF(dt,'') AS timedate,
    NULLIF(sys_type, '') AS sys_type,
    NULLIF(sys_id, '') AS sys_id,
    NULLIF(sys_country, '') AS country,
    NULLIF(sys_sunrise, '') AS sunrise,
    NULLIF(sys_sunset, '') AS sunset,
    NULLIF(timezone, '') AS timezone,
    NULLIF(id, '') AS id,
    name,
    NULLIF(cod, '') AS cod,
    NULLIF(rain_1h, '') AS rain_1h,
    NULLIF(rain_3h, '') AS rain_3h,
    NULLIF(snow_1h, '') AS snow_1h,
    NULLIF(snow_3h, '') AS snow_3h,
    insertdatetime


FROM source

)

SELECT *
FROM final

