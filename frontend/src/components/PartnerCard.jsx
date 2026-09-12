import { useNavigate } from "react-router-dom";

function PartnerCard({
  partner_id,
  name,
  type,
  state,
  district,
  address,
  contact_number,
  email,
  navigation_link,
  supported_scheme_types,
  supported_scheme_ids,
  selectedScheme,
  selectedSchemeName,
  active = true,
  eligible_for_new_applications = true,
  scheme_support_verified = true,
  scheme_support_note = "",
}) {
  const navigate = useNavigate();

  const location = [district, state].filter(Boolean).join(", ");

  const handleViewDetails = () => {
    navigate("/PartnerDetails", {
      state: {
        partner_id,
        name,
        type,
        state,
        district,
        address,
        contact_number,
        email,
        navigation_link,
        supported_scheme_types,
        supported_scheme_ids,
        selectedScheme,
        selectedSchemeName,
        active,
        eligible_for_new_applications,
      },
    });
  };

  const handleNavigate = () => {
    const destination = navigation_link ||
      `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
        `${address || ""}, ${district || ""}, ${state || ""}`
      )}`;

    window.open(destination, "_blank", "noopener,noreferrer");
  };

  const statusText = !active
    ? "Inactive"
    : eligible_for_new_applications
      ? "Accepting applications"
      : "Contact partner";

  return (
    <article className="partner-card">
      <div className="partner-card-header">
        <div>
          <span className="partner-type">{type || "Channel partner"}</span>
          <h3>{name}</h3>
        </div>
        <span className={`partner-status ${!eligible_for_new_applications ? "partner-status-warn" : ""}`}>
          {statusText}
        </span>
      </div>

      {!scheme_support_verified && scheme_support_note && (
        <div className="partner-fallback-note partner-card-note">{scheme_support_note}</div>
      )}

      <div className="partner-info">
        <div className="partner-info-item">
          <span>Partner location</span>
          <strong>{location || "Location not specified"}</strong>
        </div>

        <div className="partner-info-item">
          <span>Selected scheme</span>
          <strong>{selectedSchemeName || selectedScheme || "Scheme not specified"}</strong>
        </div>

        <div className="partner-info-item partner-address">
          <span>Address</span>
          <strong>{address || "Address not available"}</strong>
        </div>

        <div className="partner-info-item">
          <span>Contact</span>
          <strong>{contact_number || email || "Contact details not listed"}</strong>
        </div>
      </div>

      <div className="partner-card-actions">
        <button className="partner-view-button" type="button" onClick={handleViewDetails}>
          View Details →
        </button>
        <button className="partner-navigate-button" type="button" onClick={handleNavigate}>
          Navigate ↗
        </button>
      </div>
    </article>
  );
}

export default PartnerCard;
