#!/usr/bin/env python3
"""Filter_logger module
"""

import re
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """Logs message"""
    return re.sub(
        rf'({"|".join(map(re.escape, fields))})=.*?(?={re.escape(separator)})',
        lambda m: f"{m.group(1)}={redaction}", message)
