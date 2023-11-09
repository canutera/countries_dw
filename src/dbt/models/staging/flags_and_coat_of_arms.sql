-- depends_on: {{ ref('countries') }}
-- depends_on: {{ ref('flags') }}
-- depends_on: {{ ref('coat_of_arms') }}


with countries as (
    select *
    from {{(ref('countries')) }}
),


pivoted_flags as (
    select 
        *
    from crosstab(
        $$
        with flags as (
            select *
            from {{ source('raw', 'flags') }}
        )
        select 
            common_name, image_format, link
        from
            flags
        order by 
            1, 2
        $$, 
        $$
        with flags as (
            select *
            from {{ source('raw', 'flags') }}
        )
        select distinct image_format from flags order by 1 
        $$
    ) as ct (country text, flag_description text, png_flag text, svg_flag text)
),

pivoted_coat_of_arms as (
    select 
        *
    from crosstab(
        $$
        with coat_of_arms as (
            select *
            from {{ source('raw', 'coat_of_arms') }}
        )
        select 
            common_name, image_format, link
        from
            coat_of_arms
        order by 
            1, 2
        $$, 
        $$
        with coat_of_arms as (
            select *
            from {{ source('raw', 'coat_of_arms') }}
        )
        select distinct image_format from coat_of_arms order by 1 
        $$
    ) as ct (country text, png_coarms text, svg_coarms text)
),




final as (

    select 
        countries.country_id,
        pivoted_flags.*,
        pivoted_coat_of_arms.png_coarms,
        pivoted_coat_of_arms.svg_coarms

    from 
        countries
        join pivoted_flags on pivoted_flags.country = countries.common_name
        join pivoted_coat_of_arms on pivoted_coat_of_arms.country = countries.common_name

)

select * from final