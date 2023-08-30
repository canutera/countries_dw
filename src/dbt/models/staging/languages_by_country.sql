with raw_languages as (
    select * from {{source('raw', 'languages')}}
),
countries as (
    select * from {{(ref('countries'))}}
),

final as (

    select
        countries.country_id        as country_id,
        raw_languages.common_name   as country,
        raw_languages.lang          as language_name,
        raw_languages.lang_code
    from 
        raw_languages 
            join countries on raw_languages.common_name = countries.common_name
    order by
        country_id
)

select * from final
