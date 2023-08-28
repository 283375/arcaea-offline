import json
from typing import List, Optional


def recover_search_title(db_value: Optional[str]) -> List[str]:
    return json.loads(db_value) if db_value else []
