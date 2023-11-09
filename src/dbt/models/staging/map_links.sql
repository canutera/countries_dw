-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

maps as (
    select 
        *
    from crosstab(
        $$
        with maps as (
            select *
            from {{ source('raw', 'maps') }}
        )
        select 
            common_name, "site", link
        from
            maps
        order by 
            1, 2
        $$, 
        $$
        VALUES ('googleMaps'), ('openStreetMaps')
        $$
    ) as ct (country text, google_Maps text, open_Street_Maps text)
),

final as (
    select
        countries.country_id,
        maps.*
    from countries
        join maps on countries.common_name = maps.country

)

select * from final