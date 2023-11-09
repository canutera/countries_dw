-- depends_on: {{ ref('countries') }}
-- depends_on: {{ ref('regions_and_continents') }}
with countries as (
    select *
    from {{(ref('countries')) }}
),
raw_continents as (
    select *
    from {{ source('raw', 'continents') }}
),
raw_regions as (
    select *
    from {{ source('raw', 'regions') }}
),

regions_and_continents as (
    
    select distinct
        countries.country_id,
        countries.common_name as country,
        raw_continents.continents as continent,
        raw_regions.region,
        raw_regions.subregion
    from countries
        join raw_continents on raw_continents.common_name = countries.common_name
        join raw_regions on raw_regions.common_name = countries.common_name
),

rnc_model as (
    select *
    from {{(ref('regions_and_continents')) }}
),

final as (
    select 
        regions_and_continents.*,
        rnc_model.region_id
    from
        rnc_model
        join regions_and_continents
            on rnc_model.region = regions_and_continents.region
            and rnc_model.subregion = regions_and_continents.subregion
            and rnc_model.continent = regions_and_continents.continent
    order by
        regions_and_continents.country_id
)



select * from final