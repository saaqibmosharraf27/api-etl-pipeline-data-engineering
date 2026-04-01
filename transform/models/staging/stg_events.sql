-- Staging model: parse and cast raw JSON fields into typed columns.
-- One row here = one row in raw.events.

with source as (
    select
        id,
        payload,
        ingested_at::timestamp as ingested_at
    from {{ source('raw', 'events') }}
),

parsed as (
    select
        id,
        ingested_at,
        payload->>'$.id'          as event_id,
        payload->>'$.name'        as event_name,
        payload->>'$.created_at'  as created_at_raw,
        (payload->>'$.amount')::double as amount,
        payload->>'$.status'      as status
    from source
)

select
    id,
    ingested_at,
    event_id,
    event_name,
    created_at_raw::timestamp as created_at,
    amount,
    status
from parsed
