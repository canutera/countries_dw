with raw_names as (
    select * from {{source('raw', 'names')}}
),

lat_lng as (
    select *
    from {{ source('raw', 'lat_lng')}}
),

final as (

    select
        cast(row_number() over (order by raw_names.common_name) as int) as country_id,
        raw_names.*,
        lat_lng.latitude,
        lat_lng.longitude
    from 
        raw_names
        join lat_lng on lat_lng.common_name = raw_names.common_name
)

select * from final
