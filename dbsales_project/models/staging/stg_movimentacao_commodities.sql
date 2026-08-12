-- import

with source as(
    select 
        date,
        symbol,
        action,
        quantity
    from  {{source ('dbsales_project', 'movimentacao_commodities')}}
),

-- renamed

renamed as(
    select 
        cast(date as date) as data,
        symbol as simbolo,
        action as acao,
        quantity as quantidade
    from 
        source
)

-- query

select * from renamed