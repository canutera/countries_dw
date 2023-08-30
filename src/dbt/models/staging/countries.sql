with raw_names as (
    select * from {{source('raw', 'names')}}
),

final as (

    select
        cast(row_number() over (order by common_name) as int) as country_id,
        raw_names.*
    from 
        raw_names
)

select * from final
