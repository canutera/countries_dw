-- depends_on: {{ ref('countries') }}

with countries as (
    select *
    from {{(ref('countries')) }}
),

ind as (
    select *
    from {{(source('raw', 'independency_table')) }}
), 
un as (
    select *
    from {{(source('raw', 'un_membership_table')) }}
), 


final as (
    select
        countries.country_id,
        ind.common_name as country,
        ind.independent,
        un."unMember" as unmember
    from
        countries
        join ind on countries.common_name = ind.common_name
        join un on countries.common_name = un.common_name

)

select * from final