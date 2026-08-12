-- import

with source as(
    select 
        date, 
        "Close", 
        simbolo
    from  {{source ('dbsales_project', 'commodities')}}
),

-- renamed

renamed as(
    select 
        cast(date as date) as data,
        "Close" as Valor_fechamento,
        simbolo
    from 
        source
)

-- query

select * from renamed