-- depends_on: {{ ref('countries') }}
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
        raw_continents.continents as continent,
        raw_regions.region,
        raw_regions.subregion
    from countries
        join raw_continents on raw_continents.common_name = countries.common_name
        join raw_regions on raw_regions.common_name = countries.common_name
),

final as (
    select 
        row_number() 
        over (
            order by 
                regions_and_continents.continent,
                regions_and_continents.region,
                regions_and_continents.subregion
                
        ) :: int as region_id,
        regions_and_continents.continent,
        regions_and_continents.region,
        regions_and_continents.subregion
    from 
        regions_and_continents
    order by 
        region_id
)



select * from final