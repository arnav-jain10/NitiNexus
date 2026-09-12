# Scheme data verification

## Important
The matching engine now supports a **minimum loan amount** (`loan_min`) as well as a maximum. A scheme is eligible only when the requested amount is within the configured range.

The uploaded project did not contain authoritative minimum-loan values for the five seed schemes, and this build environment could not access the live NSFDC website. Therefore the seed records deliberately leave `loan_min` as `null` rather than inventing government values. When the official NSFDC scheme documents are available, populate the verified value in `backend/seed.py` and set `data_verified=True` / `last_verified` to the actual verification date.

The same principle applies to other scheme terms: the application exposes the official-source link and tells users to confirm final terms with the authorized agency. Do not mark a value as officially verified unless it has been checked against the current official document.

## Minimum-loan behavior
If `loan_min` is populated, the matching engine enforces:

`loan_min <= requested_amount <= loan_max`

A request below the minimum is placed in the ineligible list with a clear reason and cannot appear in recommendations.

## Partner data
The included SQLite database has been populated from `backend/partners_seed.csv`. The import contains 91 channel-partner records. General banking records that are not explicitly scheme-tagged are handled as a transparent location fallback and the UI asks the applicant to verify scheme support before applying.
