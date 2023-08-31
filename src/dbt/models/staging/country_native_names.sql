-- depends_on: {{ ref('languages_table') }}
with raw_native_names as (
    select * from {{source('raw', 'native_names')}}
),
countries as (
    select * from {{(ref('countries'))}}
),

languages as (
    select * from {{(ref('languages_table'))}}
),

final as (

    select
        raw_native_names.common_name as country,
        raw_native_names.official as translated_official_name,
        raw_native_names.common as translated_common_name,
        languages.language_name,
        raw_native_names.language_code as lang_code,
        countries.country_id
    from
        raw_native_names
        join countries on raw_native_names.common_name = countries.common_name
        join languages on raw_native_names.language_code = languages.lang_code
)

select * from final

