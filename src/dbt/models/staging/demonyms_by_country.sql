-- depends_on: {{ ref('countries') }}

with demonyms as (
    select * from {{source('raw', 'demonyms')}}
),
countries as (
    select * from {{(ref('countries'))}}
),


final as (

    select
        countries.country_id,
        countries.common_name as country,
        demonyms.m as demonym
    from
        demonyms
        join countries on demonyms.common_name = countries.common_name
        
)

select * from final