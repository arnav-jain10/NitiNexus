function IneligibleSchemeCard({ scheme }) {
  return (
    <article className="ineligible-card">
      <div className="ineligible-icon">!</div>
      <div className="ineligible-content">
        <div className="ineligible-heading">
          <div>
            <h3>{scheme.name}</h3>
            <span>{scheme.type || "Government scheme"}</span>
          </div>
          <span className="ineligible-badge">Not eligible</span>
        </div>
        <div className="ineligible-reasons">
          <strong>Why it does not match</strong>
          {(scheme.why_not_eligible || ["Your current profile does not meet this scheme's requirements."]).map((reason, index) => (
            <p key={index}>• {reason}</p>
          ))}
        </div>
      </div>
    </article>
  );
}

export default IneligibleSchemeCard;
