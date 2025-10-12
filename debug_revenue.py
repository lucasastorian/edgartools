"""Debug script to investigate missing total revenue in XBRL income statement."""

from edgar import *

# Get the Nvidia filing
company = Company("NVDA")
filings = company.get_filings(form="10-Q")
filing = filings[0]

print(f"Filing: {filing.form} - {filing.filing_date}")
print(f"Accession: {filing.accession_no}")
print()

# Get XBRL
xbrl = filing.xbrl()

# Get all facts for us-gaap_Revenues
print("=" * 80)
print("ALL us-gaap:Revenues facts in XBRL:")
print("=" * 80)

revenue_facts = [fact for fact in xbrl.facts if fact.concept == "us-gaap_Revenues"]

print(f"Found {len(revenue_facts)} revenue facts\n")

for i, fact in enumerate(revenue_facts, 1):
    print(f"\n--- Fact {i} ---")
    print(f"Value: {fact.value}")
    print(f"Period: {fact.period}")
    print(f"Dimensions: {fact.dimensions}")
    print(f"Has dimensions: {bool(fact.dimensions)}")

# Now check the income statement
print("\n" + "=" * 80)
print("Income Statement Revenue Rows:")
print("=" * 80)

statements = xbrl.statements
income_statement = statements.income_statement()

# Look at the underlying data
print(f"\nIncome statement has {len(income_statement.data)} rows")

revenue_rows = [row for row in income_statement.data if row.concept == "us-gaap_Revenues"]
print(f"Found {len(revenue_rows)} revenue rows in income statement\n")

for i, row in enumerate(revenue_rows, 1):
    print(f"\n--- Row {i} ---")
    print(f"Label: {row.label}")
    print(f"Dimension: {row.dimension}")
    print(f"Has dimension: {bool(row.dimension)}")

# Check if there's a fact without dimensions
print("\n" + "=" * 80)
print("Revenue facts WITHOUT dimensions (should be total):")
print("=" * 80)

no_dim_revenue = [fact for fact in revenue_facts if not fact.dimensions]
print(f"Found {len(no_dim_revenue)} revenue facts without dimensions\n")

for fact in no_dim_revenue:
    print(f"Value: {fact.value}")
    print(f"Period: {fact.period}")
    print(f"Context: {fact.context_ref}")
