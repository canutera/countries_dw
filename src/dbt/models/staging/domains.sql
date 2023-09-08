-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

domains as (
    select *
    from {{(source('raw', 'top_level_domains')) }}
), 

final as (
    select
        countries.country_id,
        domains.common_name as country,
        domains.tld
    from
        domains
        join countries on countries.common_name = domains.common_name

)

select * from final