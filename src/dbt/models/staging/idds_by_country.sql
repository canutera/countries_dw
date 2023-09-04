-- depends_on: {{ ref('countries') }}

with idds as (
    select * from {{source('raw', 'idds')}}
),
countries as (
    select * from {{(ref('countries'))}}
),


final as (

    select
        countries.country_id,
        countries.common_name as country,
        idds.root,
        idds.suffixes        
    from
        idds
        join countries on idds.common_name = countries.common_name
        
)

select * from final

