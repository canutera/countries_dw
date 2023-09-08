-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

car_info as (
    select *
    from {{source('raw', 'car_information')}}
),

final as (
    select 
        countries.country_id,
        car_info.common_name as country,
        car_info.side,
        car_info.signs
    from 
        countries
        join car_info on car_info.common_name = countries.common_name

)

select * from final