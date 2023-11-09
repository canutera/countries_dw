-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

timezones as (
    select *
    from {{(source('raw', 'timezones')) }}
), 

final as (
    select
        countries.country_id,
        timezones.common_name as country,
        timezones.timezones
    from
        timezones
        join countries on countries.common_name = timezones.common_name

)

select * from final