-- depends_on: {{ ref('countries') }}

with countries as (
    SELECT * from {{ref('countries')}}
),
codes as (
    SELECT * from {{ref('codes_by_country')}}
),

borders as (
    SELECT * from {{source('raw','borders')}}

),

final as (
    select 
        countries.country_id,
        borders.common_name as country,
        borders.borders as cca3_border,
        codes.country as country_border
        
    from
        borders
        join countries on borders.common_name = countries.common_name
        join codes on borders.borders = codes.cca3
    order by
        countries.country_id
)
select * from final