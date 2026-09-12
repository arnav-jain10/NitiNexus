import { useLocation, Link } from "react-router-dom";
import PageNavigation from "../components/PageNavigation";

function PartnerDetails() {
  const { state: partner } = useLocation();

  if (!partner) {
    return (
      <div className="page-frame">
        <div className="empty-state">
          <div className="eyebrow">PARTNER DETAILS</div>
          <h1>No partner selected</h1>
          <p>Return to the partner list and choose a channel partner.</p>
          <Link className="inline-primary" to="/partners">
            Back to Partners →
          </Link>
        </div>
      </div>
    );
  }

  const address = [partner.address, partner.district, partner.state]
    .filter(Boolean)
    .join(", ");

  const directionsUrl =
    partner.navigation_link ||
    `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`;

  const status = partner.active === false
    ? "INACTIVE"
    : partner.eligible_for_new_applications === false
      ? "CONTACT PARTNER"
      : "ACCEPTING APPLICATIONS";

  return (
    <div className="page-frame partner-details-page">
      <div className="partner-details-card">
        <div className="scheme-details-header">
          <div>
            <div className="eyebrow">CHANNEL PARTNER · 04</div>
            <h1>{partner.name}</h1>
            <p>{partner.type || "Channel partner"}</p>
          </div>
          <span className={`partner-status large ${partner.eligible_for_new_applications === false ? "partner-status-warn" : ""}`}>
            {status}
          </span>
        </div>

        <div className="detail-metrics partner-metrics">
          <div>
            <span>State</span>
            <strong>{partner.state || "—"}</strong>
          </div>
          <div>
            <span>District</span>
            <strong>{partner.district || "—"}</strong>
          </div>
          <div>
            <span>Contact</span>
            <strong>{partner.contact_number || "Not listed"}</strong>
          </div>
          <div>
            <span>Email</span>
            <strong>{partner.email || "Not listed"}</strong>
          </div>
        </div>

        <section className="detail-section">
          <div className="section-title">
            <div>
              <h2>Partner information</h2>
              <p className="section-subtitle">Location, scheme support and contact details.</p>
            </div>
          </div>

          <div className="eligibility-grid partner-detail-grid">
            <div className="wide">
              <span>Address</span>
              <strong>{partner.address || "Address not available"}</strong>
            </div>
            <div className="wide">
              <span>Selected scheme</span>
              <strong>{partner.selectedSchemeName || "Selected scheme"}</strong>
            </div>
            <div className="wide">
              <span>Supported scheme types</span>
              <strong>{(partner.supported_scheme_types || []).join(", ") || "Multiple schemes"}</strong>
            </div>
          </div>
        </section>

        <div className="partner-details-actions">
          <a className="partner-primary-button" href={directionsUrl} target="_blank" rel="noreferrer">
            Get Directions ↗
          </a>
          {partner.contact_number && (
            <a className="partner-secondary-button" href={`tel:${partner.contact_number}`}>
              Call
            </a>
          )}
          {partner.email && (
            <a className="partner-secondary-button" href={`mailto:${partner.email}`}>
              Email
            </a>
          )}
        </div>

        <div className="partner-disclaimer">
          Confirm current application availability, documents and scheme terms directly with the partner before submitting an application.
        </div>

        <PageNavigation
          backTo={`/partners?scheme=${encodeURIComponent(partner.selectedScheme || "")}`}
          nextLabel="Finish"
        />
      </div>
    </div>
  );
}

export default PartnerDetails;
