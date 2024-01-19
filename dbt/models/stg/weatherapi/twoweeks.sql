SELECT 


    coord_lon,
    coord_lat,
    weather,
    weather_description,
    weather_icon,
    base,
    temperature,
    feels_like,
    temp_min,
    temp_max,
    pressure,
    humidity,
    visibility,
    wind_speed,
    wind_direction,
    wind_gust,
    cloudiness,
    sunrise,
    sunset,
    name,
    timedate


FROM {{ref ("convert_types") }}

WHERE (date(now())-date(timedate))::numeric  < 14