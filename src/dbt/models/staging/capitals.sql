-- depends_on: {{ ref('countries') }}

with raw_capitals as (
    select * from {{source('raw', 'capital')}}
),
countries as (
    select * from {{(ref('countries'))}}
),


final as (

    select
        countries.country_id,
        countries.common_name as country,
        raw_capitals.capital,
        raw_capitals.latitude,
        
        raw_capitals.longitude
    from
        raw_capitals
        join countries on raw_capitals.common_name = countries.common_name
        
)

select * from final

