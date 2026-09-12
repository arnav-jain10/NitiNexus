# NitiNexus – Updated SIH Build

This package contains the updated frontend + backend and a populated SQLite database.

## Included changes

- Minimum-loan support in the scheme model and matching engine.
- Requested amount is rejected when below a configured `loan_min` or above `loan_max`.
- Transparent ineligible reasons.
- Partner database populated from the included 91-record seed CSV.
- Partner search now has district/state/multi-state matching plus a transparent location fallback for general banking records.
- Channel Partner page includes a real Google Maps embed without requiring a Maps API key.
- Light theme across the application.
- Dedicated FAQ page added to the main navigation.
- Scheme verification status is exposed instead of falsely claiming live official verification.

## Start backend

```bash
cd backend
python -m pip install -r requirements.txt
python migrate.py
python seed.py
python import_partners.py
uvicorn app.main:app --reload
```

The included `backend/sih26092.db` is already migrated, seeded and populated with partners, so you normally do not need to rerun the seed/import unless you intentionally want to reset the data.

## Start frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://127.0.0.1:8000` for the backend. Set `VITE_API_URL` if your backend uses another URL.

## Important scheme-data note

The uploaded project did **not** contain authoritative minimum-loan values for the five seed schemes, and this build environment could not reach the live NSFDC website. The new `loan_min` field is therefore deliberately `null` in the seed data instead of inventing government values. When you have the current official NSFDC documents, put the verified minimums and any other corrected eligibility terms into `backend/seed.py`, then mark those records verified.

See `SCHEME_DATA_VERIFICATION.md` for details.
