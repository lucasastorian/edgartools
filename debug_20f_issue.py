"""
Debug 20-F filing issue with TSM
"""

from edgar import Company, set_identity

set_identity('lucas@intellifin.ai')

print("=" * 80)
print("Debugging TSM 20-F Filing")
print("=" * 80)

# Get TSM (Taiwan Semiconductor)
tsm = Company('TSM')
filing = tsm.get_filings(form='20-F').latest(1)

print(f"\nFiling: {filing.form} - {filing.report_date}")
print(f"Accession: {filing.accession_number}")

xbrl = filing.xbrl()

print("\n" + "=" * 80)
print("ENTITY INFO")
print("=" * 80)
for key, value in xbrl.entity_info.items():
    print(f"{key}: {value}")

print("\n" + "=" * 80)
print("AVAILABLE PERIODS")
print("=" * 80)
print(f"Total reporting periods: {len(xbrl.reporting_periods)}")
for period in xbrl.reporting_periods[:10]:  # Show first 10
    print(f"\n{period}")

print("\n" + "=" * 80)
print("INCOME STATEMENT PERIODS")
print("=" * 80)

income = xbrl.statements.income_statement()
rendered = income.render(include_dimensions=False)

print(f"\nNumber of periods in rendered statement: {len(rendered.header.periods)}")
for i, period in enumerate(rendered.header.periods):
    from datetime import datetime
    duration_days = None
    if period.start_date and period.end_date:
        start = datetime.strptime(period.start_date, '%Y-%m-%d')
        end = datetime.strptime(period.end_date, '%Y-%m-%d')
        duration_days = (end - start).days

    print(f"\nPeriod {i}:")
    print(f"  key: {period.key}")
    print(f"  end_date: {period.end_date}")
    print(f"  is_duration: {period.is_duration}")
    print(f"  quarter: {period.quarter}")
    if duration_days:
        print(f"  duration_days: {duration_days}")

print("\n" + "=" * 80)
print("TEST current_period_only")
print("=" * 80)

try:
    df = income.to_dataframe(include_dimensions=False, current_period_only=True)
    date_cols = [col for col in df.columns if col not in ['concept', 'label', 'level', 'abstract', 'dimension', 'axis', 'member', 'period']]
    print(f"\nColumns with current_period_only=True: {date_cols}")

    if not date_cols:
        print("\n✗ ERROR: No date columns!")
        print("\nTrying without current_period_only...")
        df_all = income.to_dataframe(include_dimensions=False, current_period_only=False)
        all_cols = [col for col in df_all.columns if col not in ['concept', 'label', 'level', 'abstract', 'dimension', 'axis', 'member', 'period']]
        print(f"Available columns: {all_cols}")

        # Check document_period_end_date vs actual period dates
        doc_end = xbrl.entity_info.get('document_period_end_date')
        print(f"\ndocument_period_end_date: {doc_end}")
        print(f"Period end dates: {[p.end_date for p in rendered.header.periods]}")

        # Check if there's a mismatch
        if doc_end not in [p.end_date for p in rendered.header.periods]:
            print(f"\n⚠️ MISMATCH: document_period_end_date ({doc_end}) doesn't match any period end_date!")
    else:
        print("✓ Success!")

except Exception as e:
    print(f"\n✗ Exception: {e}")
    import traceback
    traceback.print_exc()
