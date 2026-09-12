import { useLocation, Link } from "react-router-dom";
import { useState } from "react";
import { api } from "../api";
import PageNavigation from "../components/PageNavigation";

const money = (value) =>
  value === null || value === undefined
    ? "N/A"
    : `₹${Number(value).toLocaleString("en-IN")}`;

function SchemeDetails() {
  const { state } = useLocation();
  const scheme = state || JSON.parse(sessionStorage.getItem("selectedScheme") || "null");

  const profile = JSON.parse(
    sessionStorage.getItem("profileData") || "null"
  );

  const [emi, setEmi] = useState(null);
  const [emiLoading, setEmiLoading] = useState(false);

  if (!scheme) {
    return (
      <div className="page-frame">
        <div className="empty-state">
          <div className="eyebrow">SCHEME DETAILS</div>

          <h1>No scheme selected</h1>

          <p>
            Return to recommendations and choose a scheme.
          </p>

          <Link className="inline-primary" to="/dashboard">
            Back to Results
          </Link>
        </div>
      </div>
    );
  }

  const loanAmount = Number(profile?.amount || 0);

  const calculateEmi = async () => {
    if (!loanAmount || loanAmount <= 0) {
      return alert(
        "Your requested amount is missing. Please review your profile."
      );
    }

    if (scheme.loan_min != null && loanAmount < Number(scheme.loan_min)) {
      return alert(
        `Your requested amount is below this scheme's minimum loan of ${money(scheme.loan_min)}.`
      );
    }

    if (
      scheme.loan_max &&
      loanAmount > Number(scheme.loan_max)
    ) {
      return alert(
        `Your requested amount exceeds this scheme's maximum loan of ${money(
          scheme.loan_max
        )}.`
      );
    }

    setEmiLoading(true);

    try {
      setEmi(
        await api.calculateEmi(
          loanAmount,
          Number(
            scheme.interest_rate_beneficiary_percent || 0
          ),
          Number(scheme.tenure_years || 1)
        )
      );
    } catch (error) {
      alert(`Could not calculate EMI: ${error.message}`);
    } finally {
      setEmiLoading(false);
    }
  };

  const officialSourceUrl = scheme.source_url?.includes(
    "nsfdc.nic.in"
  )
    ? "https://nsfdc.nic.in/"
    : scheme.source_url;

  return (
    <div className="page-frame scheme-details-page">
      <div className="scheme-details-card">

        {/* =========================
            HEADER
        ========================== */}
        <div className="scheme-details-header">
          <div>
            <div className="eyebrow">
              SCHEME DETAILS · 03
            </div>

            <h1>{scheme.name}</h1>

            <p>
              {scheme.type} ·{" "}
              {scheme.implementing_body ||
                "Authorized agency"}
            </p>
          </div>

          <span className="match-badge">
            ✓ {scheme.match_percent}% match
          </span>
        </div>

        {/* =========================
            SCHEME METRICS
        ========================== */}
        <div className="scheme-source-note">
          <span>{scheme.data_verified ? "Official data context" : "Verification status"}</span>
          <strong>{scheme.data_verified ? "Verify final terms and document requirements with the authorized agency or channel partner." : "Some scheme values are pending verification against the current official source. Confirm all terms before applying."}</strong>
        </div>

        <div className="detail-metrics">
          <div>
            <span>Loan range</span>
            <strong>
              {scheme.loan_min != null ? `${money(scheme.loan_min)} – ${money(scheme.loan_max)}` : `Up to ${money(scheme.loan_max)}`}
            </strong>
          </div>

          <div>
            <span>Beneficiary interest</span>
            <strong>
              {scheme.interest_rate_beneficiary_percent ??
                "N/A"}
              %
            </strong>
          </div>

          <div>
            <span>Maximum tenure</span>
            <strong>
              {scheme.tenure_years ?? "N/A"} years
            </strong>
          </div>

          <div>
            <span>Your requested amount</span>
            <strong>
              {money(loanAmount)}
            </strong>
          </div>
        </div>

        {/* =========================
            WHY THIS SCHEME MATCHES
        ========================== */}
        <section className="detail-section">
          <div className="section-title">
            <div>
              <h2>Why this scheme matches</h2>

              <p className="section-subtitle">
                The strongest signals from your profile.
              </p>
            </div>
          </div>

          <div className="reason-grid">
            {(scheme.why_recommended || []).map(
              (reason, i) => (
                <div
                  className="reason-item"
                  key={i}
                >
                  <span>✓</span>
                  <p>{reason}</p>
                </div>
              )
            )}
          </div>
        </section>

        {/* =========================
            ELIGIBILITY SNAPSHOT
        ========================== */}
        <section className="detail-section">
          <div className="section-title">
            <div>
              <h2>Your eligibility snapshot</h2>

              <p className="section-subtitle">
                The information used in this
                recommendation.
              </p>
            </div>
          </div>

          <div className="eligibility-grid">
            <div>
              <span>Category</span>
              <strong>
                {profile?.caste || "N/A"}
              </strong>
            </div>

            <div>
              <span>Annual income</span>
              <strong>
                {money(profile?.income)}
              </strong>
            </div>

            <div>
              <span>Age</span>
              <strong>
                {profile?.age
                  ? `${profile.age} years`
                  : "Not provided"}
              </strong>
              <small className="eligibility-note">Checked only when an official scheme age rule is available.</small>
            </div>

            <div>
              <span>Purpose</span>
              <strong>
                {profile?.purpose || "N/A"}
              </strong>
            </div>
          </div>
        </section>

        {/* =========================
            DOCUMENTS REQUIRED
        ========================== */}
        <section className="detail-section">
          <div className="section-title">
            <div>
              <h2>Documents Generally Required</h2>

              <p className="section-subtitle">
                Keep these documents ready. Exact requirements may vary by
                implementing agency, channel partner and applicant.
              </p>
            </div>
          </div>

          {scheme.documents_required &&
          scheme.documents_required.length > 0 ? (
            <div className="reason-grid">
              {scheme.documents_required.map(
                (document, i) => (
                  <div
                    className="reason-item"
                    key={i}
                  >
                    <span>✓</span>

                    <p>{document}</p>
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="empty-state">
              <p>
                Document information is currently
                unavailable. Please verify the
                requirements with the official source.
              </p>
            </div>
          )}
        </section>

        {/* =========================
            EMI CALCULATOR
        ========================== */}
        <section className="detail-section emi-panel">
          <div className="section-title">
            <div>
              <h2>Estimated EMI</h2>

              <p className="section-subtitle">
                Based on your requested amount and
                this scheme's rate and tenure.
              </p>
            </div>
          </div>

          <div className="emi-row">
            <div className="emi-input-display">
              <span>Requested amount</span>

              <strong>
                {money(loanAmount)}
              </strong>
            </div>

            <button
              onClick={calculateEmi}
              disabled={emiLoading}
            >
              {emiLoading
                ? "Calculating..."
                : "Calculate EMI"}
            </button>
          </div>

          {emi && (
            <div className="emi-result">
              <div>
                <span>Monthly EMI</span>

                <strong>
                  {money(emi.monthly_emi)}
                </strong>
              </div>

              <div>
                <span>Total interest</span>

                <strong>
                  {money(emi.total_interest)}
                </strong>
              </div>

              <div>
                <span>Total payable</span>

                <strong>
                  {money(emi.total_payable)}
                </strong>
              </div>
            </div>
          )}
        </section>

        {/* =========================
            OFFICIAL SOURCE
        ========================== */}
        <div className="source-row">
          <span>
            Verify scheme information with the
            official source.
          </span>

          {officialSourceUrl && (
            <a
              href={officialSourceUrl}
              target="_blank"
              rel="noreferrer"
            >
              Official Source ↗
            </a>
          )}
        </div>

        {/* =========================
            NEXT NAVIGATION
        ========================== */}
        <PageNavigation
          nextTo={`/partners?scheme=${encodeURIComponent(
            scheme.scheme_id
          )}`}
          nextLabel="Next: Partners"
        />

      </div>
    </div>
  );
}

export default SchemeDetails;