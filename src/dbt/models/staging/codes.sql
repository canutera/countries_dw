with raw_codes as (
    select * from {{source('raw', 'codes')}}
),
countries as (
    select * from {{(ref('countries'))}}
),


final as (

    select
        countries.country_id,
        countries.common_name as country,
        cast (raw_codes.cca2 as varchar(2)) as cca2,
        cast (raw_codes.cca3 as varchar(3)) as cca3,
        cast (raw_codes.ccn3 as varchar(3)) as ccn3,
        cast (raw_codes.cioc as varchar(3)) as cioc,
        cast (raw_codes.fifa as varchar(3)) as fifa,
        raw_codes.status
    from
        raw_codes
        join countries on raw_codes.common_name = countries.common_name
        
)

select * from final