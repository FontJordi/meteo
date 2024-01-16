{{ config(materialized='table') }}

select
idcode,  coord_lon ,  coord_lat ,  weather_id ,  weather_main ,
         weather_description ,  weather_icon ,  base ,  main_temp ,
         main_feels_like ,  main_temp_min ,  main_temp_max ,  main_pressure ,
         main_humidity ,  main_sea_level ,  main_grnd_level ,  visibility ,
         wind_speed ,  wind_deg ,  wind_gust ,  clouds_all , 
        
        TO_TIMESTAMP(dt::numeric) as dt,
        
         sys_type ,
         sys_id ,  sys_country ,  sys_sunrise ,  sys_sunset ,  timezone ,  id ,
         name , cod 

from meteo_hist as t1