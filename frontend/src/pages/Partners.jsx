import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import PartnerCard from "../components/PartnerCard";
import PageNavigation from "../components/PageNavigation";
import { api } from "../api";

const SCHEME_NAMES = {
  SCH001: "Micro Finance Scheme (MFS)",
  SCH002: "Term Loan",
  SCH003: "Aajeevika Micro-Finance Yojana (AMY)",
  SCH004: "Udyam Nidhi Yojana (UNY)",
  SCH005: "Educational Loan Scheme (ELS)",
};

function Partners() {
  const [searchParams] = useSearchParams();
  const schemeId = searchParams.get("scheme") || "";

  const profile = useMemo(
    () => JSON.parse(sessionStorage.getItem("profileData") || "null"),
    []
  );

  const [partners, setPartners] = useState([]);
  const [scope, setScope] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!schemeId) {
      setLoading(false);
      setError("No scheme was selected. Return to your recommendations and choose a scheme first.");
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError("");

    api.getPartners({
      state: profile?.state || "",
      district: profile?.district || "",
      schemeId,
    })
      .then((data) => {
        if (cancelled) return;
        setPartners(data.partners || []);
        setScope(data.scope || "");
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [schemeId, profile?.state, profile?.district]);

  const schemeName = SCHEME_NAMES[schemeId] || schemeId || "Selected scheme";
  const locationText = [profile?.district, profile?.state].filter(Boolean).join(", ");

  if (!schemeId) {
    return (
      <div className="page-frame partners-page">
        <div className="partners-card empty-state">
          <div className="eyebrow">CHANNEL PARTNERS · 04</div>
          <h1>Select a scheme first</h1>
          <p>{error}</p>
          <Link className="inline-primary" to="/dashboard">
            Back to Recommendations →
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page-frame partners-page">
      <div className="partners-card">
        <div className="partners-header">
          <div>
            <div className="eyebrow">CHANNEL PARTNERS · 04</div>
            <h1>Find a channel partner</h1>
            <p>
              We use your selected scheme and profile location automatically, so you do not have to enter the same information again.
            </p>
          </div>
          <span className="status-pill">
            <span className="online-dot" /> Partner search online
          </span>
        </div>

        <section className="partner-context" aria-label="Partner search context">
          <div className="partner-context-item">
            <span>Selected scheme</span>
            <strong>{schemeName}</strong>
          </div>
          <div className="partner-context-item">
            <span>Your location</span>
            <strong>{locationText || "Location not available"}</strong>
          </div>
          <div className="partner-context-item">
            <span>Search scope</span>
            <strong>{scope ? scope.replace("-", " ") : "Finding nearby partners"}</strong>
          </div>
        </section>

        <section className="nearby-partners-section">
          <div className="section-title">
            <div>
              <h2>Available channel partners</h2>
              <p className="section-subtitle">
                Partners are filtered for the selected scheme and your saved location.
              </p>
            </div>
            <span className="count-chip">
              {loading ? "Searching…" : `${partners.length} found`}
            </span>
          </div>

          {!loading && !error && scope.includes("fallback") && (
            <div className="partner-fallback-note">
              <strong>Location fallback:</strong> No explicitly scheme-tagged partner was found for this area. These partners are listed for your location; confirm that they currently handle the selected scheme before applying.
            </div>
          )}

          {loading ? (
            <div className="no-partners loading-state">
              <span className="spinner" />
              <h3>Finding suitable partners…</h3>
              <p>Checking the partner directory for your scheme and location.</p>
            </div>
          ) : error ? (
            <div className="no-partners">
              <h3>Unable to load partners</h3>
              <p>{error}</p>
              <Link className="inline-primary" to="/dashboard">
                Back to Results
              </Link>
            </div>
          ) : partners.length ? (
            <div className="partner-list">
              {partners.map((partner) => (
                <PartnerCard
                  key={partner.partner_id}
                  {...partner}
                  selectedScheme={schemeId}
                  selectedSchemeName={schemeName}
                />
              ))}
            </div>
          ) : (
            <div className="no-partners">
              <h3>No partner found in this area</h3>
              <p>
                No active partner is currently listed for this scheme in the available directory. Check the official scheme source or try again later.
              </p>
            </div>
          )}

          {!loading && !error && (
            <section className="partner-map-section">
              <div className="section-title">
                <div>
                  <h2>Location map</h2>
                  <p className="section-subtitle">Map view for your selected location and available partners.</p>
                </div>
              </div>
              <div className="partner-map-container">
                <iframe
                  title="Channel partner location map"
                  src={`https://www.google.com/maps?q=${encodeURIComponent(
                    partners[0]?.address || locationText || "India"
                  )}&output=embed`}
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                />
              </div>
            </section>
          )}
        </section>

        <div className="partner-disclaimer">
          <strong>Important:</strong> Partner availability and application acceptance can change. Confirm current eligibility, documents and application availability directly with the authorized partner before applying.
        </div>

        <PageNavigation
          backTo={`/scheme-details`}
          nextTo="/"
          nextLabel="Finish"
        />
      </div>
    </div>
  );
}

export default Partners;
