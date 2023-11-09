with raw_languages as (
    select * from {{source('raw', 'languages')}}
),

final as (
    select distinct on (lang_code)
        lang as language_name,
        lang_code
    from 
        raw_languages
    order by
        lang_code
)

select * from final