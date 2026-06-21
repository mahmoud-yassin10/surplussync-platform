# Impact Methodology

## Lifecycle States

SurplusSync separates forecast, proposed, approved, scheduled, and confirmed states.

## Value Labels

Values are labeled as observed, calculated, projected, or synthetic/demo. A recommendation is not automatically meals saved, and scheduled pickup is not confirmed delivery.

## Formulas

- Preventable meals: `normal preparation - recommended preparation`
- Recovered meals: confirmed recovered meals after eligible pickup completion
- Nonrecoverable waste: confirmed surplus that cannot be safely recovered
- Cost estimate: meal count multiplied by disclosed local assumption
- Duplicate prevention: repeated confirmation does not double-count impact

## Carbon

Carbon impact is estimated, not measured. The current basis assumes 1.2 lb per meal, converts pounds to kilograms, and applies a ReFED-derived scenario factor. Prevented and recovered meals are included in the current calculation basis.

Sources preserved in code and docs:

- ReFED Impact Calculator meals-recovered methodology
- ReFED food-waste climate reduction scenario

The carbon ledger is not audited carbon accounting.

## Annualization

Annualized figures must be labeled projected and must not be presented as observed impact.
