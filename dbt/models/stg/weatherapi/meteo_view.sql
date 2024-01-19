{{ config(materialized='view') }}

WITH CTE AS(

        SELECT *
        FROM {{ref ("convert_types") }}

), final AS (

        select
                name as Name,
                coord_lon::numeric as Lon,
                coord_lat::numeric as Lat,
                weather as Weather,
                weather_description as Weather_Description,
                temperature::numeric as temperature,
                feels_like::numeric as Temp_feels_like,
                temp_min::numeric as Temp_min,
                temp_max::numeric as Temp_max,
                pressure::numeric as Pressure,
                humidity::numeric as Humidity,
                visibility::numeric as Visibility,
                wind_speed::numeric as Wind_Speed,
                wind_direction::numeric as Wind_Direction,
                cloudiness::numeric as Cloudiness,
                timedate,
                sunrise,
                sunset

        FROM cte
)

select * from final