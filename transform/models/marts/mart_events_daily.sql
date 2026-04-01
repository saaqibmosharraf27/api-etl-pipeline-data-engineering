-- Mart model: daily aggregation of events for reporting.

with events as (
    select * from {{ ref('stg_events') }}
),

daily as (
    select
        created_at::date          as event_date,
        status,
        count(*)                  as event_count,
        sum(amount)               as total_amount,
        avg(amount)               as avg_amount
    from events
    group by 1, 2
)

select
    event_date,
    status,
    event_count,
    round(total_amount, 2) as total_amount,
    round(avg_amount, 2)   as avg_amount
from daily
order by event_date desc, status
