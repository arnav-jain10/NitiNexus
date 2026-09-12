import { useNavigate } from "react-router-dom";

function SchemeCard({ scheme }) {
  const navigate = useNavigate();

  const openDetails = () => {
    sessionStorage.setItem("selectedScheme", JSON.stringify(scheme));
    navigate("/scheme-details", { state: scheme });
  };

  return (
    <article className="scheme-card">
      <span className="recommended-badge">
        ✓ Recommended · {scheme.match_percent}% match
      </span>

      <h3>{scheme.name}</h3>
      <p className="scheme-description">
        {scheme.type || "Government financial assistance scheme"}
      </p>

      <div className="scheme-summary">
        <div>
          <strong>Loan Range</strong>
          <p>{scheme.loan_min != null ? `₹${Number(scheme.loan_min).toLocaleString("en-IN")} – ` : "Up to "}₹{Number(scheme.loan_max || 0).toLocaleString("en-IN")}</p>
        </div>
        <div>
          <strong>Interest Rate</strong>
          <p>{scheme.interest_rate_beneficiary_percent ?? "N/A"}%</p>
        </div>
        <div>
          <strong>Tenure</strong>
          <p>{scheme.tenure_years ?? "N/A"} years</p>
        </div>
      </div>

      <div className="recommendation-box">
        <h4>Why is this scheme recommended?</h4>
        {(scheme.why_recommended || []).map((reason, index) => (
          <p key={index}>✓ {reason}</p>
        ))}
      </div>

      <div className="scheme-actions">
        <button type="button" onClick={openDetails}>
          View Details →
        </button>
      </div>
    </article>
  );
}

export default SchemeCard;
