-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

infos as (
    select *
    from {{(source('raw', 'general_information')) }}

),

final as (
    select 
        countries.country_id,
        infos.common_name as country,
        infos.landlocked,
        infos.area,
        infos.flag as flag_emoji,
        infos.population,
        infos."startOfWeek" as start_of_week
    from 
        infos
        join countries on countries.common_name = infos.common_name

)

select * from final

