-- depends_on: {{ ref('countries') }}
-- depends_on: {{ ref('currencies') }}
with countries as (
    select *
    from {{(ref('countries')) }}
),
currencies as (
    select *
    from {{ source('raw', 'currencies') }}
),

final as (
    select 
        countries.country_id,
        countries.common_name as country,
        currencies.name as currency_name,
        currencies.symbol,
        currencies.currency_code
    from 
        countries
        join currencies on currencies.common_name = countries.common_name

)

select * from final