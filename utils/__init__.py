"""Utils module for SocksQuads CRM."""

from .helpers import (
    AuthenticationManager,
    initialize_session_state,
    format_currency,
    format_number,
    calculate_metrics,
    get_salesman_stats,
    get_area_stats
)
from .charts import (
    sales_by_day_chart,
    sales_by_month_chart,
    top_salesman_chart,
    top_retailer_chart,
    sales_by_area_chart
)

__all__ = [
    'AuthenticationManager',
    'initialize_session_state',
    'format_currency',
    'format_number',
    'calculate_metrics',
    'get_salesman_stats',
    'get_area_stats',
    'sales_by_day_chart',
    'sales_by_month_chart',
    'top_salesman_chart',
    'top_retailer_chart',
    'sales_by_area_chart'
]
