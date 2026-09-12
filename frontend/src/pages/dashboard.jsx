import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ProgressStep from "../components/ProgressStep";
import SchemeCard from "../components/SchemeCard";
import IneligibleSchemeCard from "../components/IneligibleSchemeCard";
import { api } from "../api";
import PageNavigation from "../components/PageNavigation";

const money = (value) => `₹${Number(value || 0).toLocaleString("en-IN")}`;

function Dashboard() {
  const [profileData, setProfileData] = useState(null);
  const [matches, setMatches] = useState([]);
  const [ineligible, setIneligible] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const profile = JSON.parse(sessionStorage.getItem("profileData") || "null");
    const profileId = sessionStorage.getItem("profileId");
    if (!profile || !profileId) {
      setLoading(false);
      return;
    }
    setProfileData(profile);
    api.match(profileId)
      .then((data) => {
        setResult(data);
        setMatches(data.top_matches || []);
        setIneligible(data.ineligible_schemes || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (!profileData) {
    return (
      <div className="page-frame dashboard-container">
        <div className="dashboard-card missing-data">
          <div className="eyebrow">SESSION REQUIRED</div>
          <h1>Start with your profile</h1>
          <p>Complete the profile once and we will compare it with every available scheme.</p>
          <Link className="inline-primary" to="/profile">Go to Profile →</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page-frame dashboard-container">
      <div className="dashboard-card">
        <ProgressStep currentStep={2} />
        <div className="dashboard-header dashboard-hero">
          <div>
            <div className="eyebrow">MATCHING ENGINE · RESULTS</div>
            <h1>Your scheme recommendations</h1>
            <p>We checked the available schemes against category, income, purpose and requested support amount.</p>
          </div>
          <div className="status-pill"><span className="online-dot" /> Match complete</div>
        </div>

        <div className="metrics-row">
          <div className="metric-card"><span>Eligible</span><strong>{result?.eligible_count ?? "—"}</strong><small>schemes match your profile</small></div>
          <div className="metric-card"><span>Not eligible</span><strong>{result?.ineligible_count ?? "—"}</strong><small>with reasons explained below</small></div>
          <div className="metric-card"><span>Requested</span><strong>{money(profileData.amount)}</strong><small>financial support</small></div>
        </div>

        <section className="summary-section compact-summary">
          <div className="section-title"><h2>Profile snapshot</h2><span>Information used for matching</span></div>
          <div className="summary-grid">
            <div className="summary-item"><span>Name</span><strong>{profileData.name}</strong></div>
            <div className="summary-item"><span>Age</span><strong>{profileData.age ? `${profileData.age} years` : "Not provided"}</strong><small>Not used for eligibility</small></div>
            <div className="summary-item location-summary"><span>Location</span><strong>{profileData.state}</strong><small>{profileData.district}</small></div>
            <div className="summary-item"><span>Category</span><strong>{profileData.caste}</strong></div>
            <div className="summary-item"><span>Annual Income</span><strong>{money(profileData.income)}</strong></div>
            <div className="summary-item"><span>Purpose</span><strong>{profileData.purpose}</strong></div>
          </div>
        </section>

        <section className="schemes-section">
          <div className="section-title">
            <div><h2>Recommended schemes</h2><p className="section-subtitle">Best matches are shown first.</p></div>
            <span className="count-chip">{matches.length} shown</span>
          </div>
          {loading ? (
            <div className="no-schemes loading-state"><span className="spinner" /><h3>Comparing schemes...</h3><p>Checking your profile against the available eligibility rules.</p></div>
          ) : error ? (
            <div className="no-schemes"><h3>Unable to load recommendations</h3><p>{error}</p><button onClick={() => navigate("/profile")}>Review Profile</button></div>
          ) : matches.length ? (
            <div className="scheme-list">{matches.map((scheme) => <SchemeCard key={scheme.scheme_id} scheme={scheme} />)}</div>
          ) : (
            <div className="no-schemes"><h3>No eligible schemes found</h3><p>See the section below to understand which requirements were not met.</p></div>
          )}
        </section>

        {!loading && !error && (
          <section className="ineligible-section">
            <div className="section-title">
              <div><h2>Not eligible for these schemes</h2><p className="section-subtitle">Transparency matters — here is exactly why a scheme did not match.</p></div>
              <span className="count-chip muted">{ineligible.length} schemes</span>
            </div>
            {ineligible.length ? <div className="ineligible-list">{ineligible.map((scheme) => <IneligibleSchemeCard key={scheme.scheme_id} scheme={scheme} />)}</div> : <div className="all-clear">✓ Your profile meets the eligibility checks for all available schemes.</div>}
          </section>
        )}

        <p className="api-disclaimer">Eligibility is based on the scheme rules and profile information currently available. Final approval is decided by the authorized scheme or channel partner.</p>
        <PageNavigation onNext={() => {
          if (matches.length) {
            sessionStorage.setItem("selectedScheme", JSON.stringify(matches[0]));
            navigate("/scheme-details", { state: matches[0] });
          }
        }} nextLabel={matches.length ? "Next: Scheme Details" : "Review Profile"} nextDisabled={!matches.length} />
      </div>
    </div>
  );
}

export default Dashboard;
