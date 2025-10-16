"""
Updated Company class to use the new get_filings_async() method from edgartools.

This eliminates the "async call made without an async bucket" warnings.
"""

import os
import aiohttp
import asyncio
from datetime import date
from typing import List, Optional, Dict
from edgar import Company as EdgarCompany
from edgar.entity.filings import EntityFilings, EntityFiling
from edgar.async_api import get_company_async

# ... (keep all your existing imports and locks)

class Company:
    forms: List[str] = ["10-K", "10-Q",
                        "8-K",
                        "DEF 14A",
                        "20-F", "6-K"]

    def __init__(self, symbol: str, database, edgar_user_agent: str, start_year: int = 2015,
                 end_year: int = 2027, verbose: bool = True):
        self.symbol = symbol.upper()
        self.database = database
        self.edgar_user_agent = edgar_user_agent
        self.start_year = start_year
        self.end_year = end_year
        self.verbose = verbose

    # ... (keep all your other methods)

    async def _load_filings(self, edgar_company: EdgarCompany, forms: Optional[List[str]] = None,
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None) -> EntityFilings:
        """Load filings from EDGAR without blocking the event loop."""
        forms_to_load = forms if forms else self.forms

        if start_date or end_date:
            start_year = date.fromisoformat(start_date).year if start_date else self.start_year
            end_year = date.fromisoformat(end_date).year if end_date else (self.end_year - 1)
            start_year = max(start_year, self.start_year)
            end_year = min(end_year, self.end_year - 1)
            years = list(range(start_year, end_year + 1)) if start_year <= end_year else []
        else:
            years = list(range(self.start_year, self.end_year))

        # NEW: Use the built-in get_filings_async() method instead of load_full_filings_async + get_filings
        # This ensures all network calls are made asynchronously without triggering sync fallbacks
        return await edgar_company.get_filings_async(form=forms_to_load, year=years)

    # ... (keep all your other methods)
