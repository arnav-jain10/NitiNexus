import { useState } from "react";
import { useNavigate } from "react-router-dom";
import InputField from "../components/InputField";
import Dropdown from "../components/Dropdown";
import ProgressStep from "../components/ProgressStep";
import { api } from "../api";
import PageNavigation from "../components/PageNavigation";
import { LOCATION_DATA, STATES } from "../locations";

function Profile() {
  const saved = JSON.parse(sessionStorage.getItem("profileData") || "null");
  const [name, setName] = useState(saved?.name || "");
  const [age, setAge] = useState(saved?.age || "");
  const [state, setState] = useState(saved?.state || "");
  const [district, setDistrict] = useState(saved?.district || "");
  const [caste, setCaste] = useState(saved?.caste || "");
  const [income, setIncome] = useState(saved?.income || "");
  const [purpose, setPurpose] = useState(saved?.purpose || "");
  const [amount, setAmount] = useState(saved?.amount || "");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const districts = state ? LOCATION_DATA[state] || [] : [];

  const submitProfile = async () => {
    if (!name || !age || !state || !district || !caste || !income || !purpose || !amount) {
      alert("Please complete all fields before continuing.");
      return;
    }
    if (Number(age) < 1 || Number(age) > 120) {
      alert("Please enter a valid age.");
      return;
    }
    if (Number(income) < 0 || Number(amount) <= 0) {
      alert("Please enter valid income and support amount.");
      return;
    }

    setLoading(true);
    try {
      const data = await api.createProfile({
        age: Number(age),
        state: state.trim(),
        district: district.trim(),
        annual_income: Number(income),
        requested_amount: Number(amount),
        category: caste,
        purpose,
        business_education: purpose === "Education" ? "education" : "business",
      });

      sessionStorage.setItem("profileData", JSON.stringify({
        name, age, state, district, caste, income, purpose, amount,
      }));
      sessionStorage.setItem("profileId", String(data.profile_id));
      sessionStorage.setItem("detailsData", JSON.stringify({ purpose, amount }));
      navigate("/dashboard");
    } catch (error) {
      console.error("Profile API Error:", error);
      alert(`Could not save your profile: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-frame form-page">
      <div className="form-card">
        <ProgressStep currentStep={1} />
        <div className="form-header">
          <div className="eyebrow">PROFILE SETUP · 01</div>
          <h1>Tell us about yourself</h1>
          <p>One short profile gives the matching engine everything it needs to find suitable financial schemes.</p>
        </div>

        <div className="form-section-label"><span>Personal information</span><small>Required</small></div>
        <div className="form-fields form-grid-2">
          <InputField label="Full Name" placeholder="Enter your name" value={name} onChange={(e) => setName(e.target.value)} />
          <InputField label="Age (informational only)" type="number" placeholder="Enter your age" value={age} onChange={(e) => setAge(e.target.value)} />
          <Dropdown label="State" value={state} onChange={(e) => { setState(e.target.value); setDistrict(""); }} options={STATES} />
          <Dropdown label="District" value={district} onChange={(e) => setDistrict(e.target.value)} options={districts} />
          <Dropdown label="Category" value={caste} onChange={(e) => setCaste(e.target.value)} options={["General", "OBC", "SC", "ST"]} />
          <InputField label="Annual Family Income" type="number" placeholder="e.g. 300000" value={income} onChange={(e) => setIncome(e.target.value)} />
        </div>

        <div className="form-section-label"><span>Financial requirement</span><small>Used for scheme matching</small></div>
        <div className="form-fields form-grid-2 requirement-fields">
          <Dropdown label="Purpose of financial support" value={purpose} onChange={(e) => setPurpose(e.target.value)} options={["Start a Business", "Expand a Business", "Education"]} />
          <InputField label="Amount of financial support needed" type="number" placeholder="e.g. 100000" value={amount} onChange={(e) => setAmount(e.target.value)} />
        </div>

        <div className="form-note"><span>i</span><p>Your state and district will also be used automatically when finding nearby channel partners.</p></div>
        <PageNavigation onNext={submitProfile} nextLabel={loading ? "Saving..." : "Next: Results"} nextDisabled={loading} />
      </div>
    </div>
  );
}

export default Profile;
