from enum import Enum
from datetime import datetime, timedelta
from typing import List


class PricingServiceLogTable(Enum):
    staging = 'RAW_TEST.STAGING__PRICING_SERVICE_V2__PUBLIC.VIEW_STAGING__PRICING_SERVICE_LOG'
    prod = 'RAW.PRICING_SERVICE_V2__PUBLIC.VIEW_PRICING_SERVICE_LOG'

def create_seed_id_query_from_pricing_service_log_table(
        seed_ids: List[str],
        table_name: PricingServiceLogTable = None,
        date: datetime.date = None
) -> str:
    quoted_seed_ids = map(lambda seed_id: f"'{seed_id}'", seed_ids)
    seed_ids_joined = ",".join(quoted_seed_ids)
    table_name = table_name if table_name else PricingServiceLogTable.staging
    date = date if date else (datetime.today().date() - timedelta(days=-7))
    return f"""
    with parsed_json as (select ID,
                                try_parse_json(OUTPUT_OBJ) as OUTPUT_OBJ,
                                try_parse_json(INPUT_OBJ)  as INPUT_OBJ,
                                CREATION_TS
                         from {table_name.value}
                         where product = 'slr-alloy' and CREATION_TS > '{date.isoformat()}')
    select
        id,
        VALUE:attributeValue::string as seed_id,
        OUTPUT_OBJ,
        INPUT_OBJ,
        CREATION_TS
    from parsed_json, lateral flatten(input => INPUT_OBJ:Earnest_Meta)
    where
        VALUE:attributeName = 'seedId' and VALUE:attributeValue::string in (
            {seed_ids_joined}
        )
    order by seed_id, CREATION_TS desc;
    """
