with raw_alt_spellings as (
    select * from {{source('raw', 'alt_spellings')}}
),
countries as (
    select * from {{(ref('countries'))}}
),


final as (

    select
        countries.common_name as country,
        raw_alt_spellings."altSpellings" as alt_spellings,
        countries.country_id
    from
        raw_alt_spellings
        join countries on raw_alt_spellings.common_name = countries.common_name
        
)

select * from final