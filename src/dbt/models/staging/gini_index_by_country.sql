-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

gini as (
    select *
    from {{(source('raw', 'gini_index')) }}
), 

final as (
    select
        countries.country_id,
        gini.common_name as country,
        gini.year,
        gini.index :: decimal
    from
        gini
        join countries on countries.common_name = gini.common_name

)

select * from final