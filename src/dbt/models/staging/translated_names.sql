-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

languages as (
    select *
    from {{(ref('languages_table')) }}
),
translations as (
    select *
    from {{source('raw', 'translations')}}
),

final as (
    select 
        countries.country_id,
        translations.common_name as country,
        translations.official,
        translations.common,
        translations.language_code,
        languages.language_name

    from 
        translations
        join countries on translations.common_name = countries.common_name
        join languages on translations.language_code = languages.lang_code

)

select * from final