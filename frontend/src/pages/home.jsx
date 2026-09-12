import PageNavigation from "../components/PageNavigation";

function Home() {
  return (
    <div className="page-frame home-page">
      <div className="home-hero">
        <div className="hero-copy">
          <div className="eyebrow">SIH 26092 · SCHEME DISCOVERY</div>
          <h1>Find financial support that fits <span>your profile.</span></h1>
          <p>One guided profile. Clear eligibility. Relevant government schemes and nearby channel partners — without repeating the same information.</p>
          <PageNavigation />
        </div>
        <div className="hero-panel">
          <div className="panel-top"><span className="online-dot" /> How NitiNexus helps <span>3 STEPS</span></div>
          <div className="landing-steps">
            <div className="landing-step"><span className="landing-step-icon">01</span><div><strong>Build your profile</strong><p>Tell us your category, income, location and funding need once.</p></div></div>
            <div className="landing-step"><span className="landing-step-icon">02</span><div><strong>Match government schemes</strong><p>See eligible schemes first, with the exact reasons behind the match.</p></div></div>
            <div className="landing-step"><span className="landing-step-icon">03</span><div><strong>Move to action</strong><p>Check documents, estimate EMI and locate an authorised channel partner.</p></div></div>
          </div>
          <div className="hero-callout"><strong>Built for clarity, not paperwork.</strong><span>Your information follows you through the entire discovery journey.</span></div>
        </div>
      </div>
      <div className="feature-strip">
        <div><span>01</span><strong>Eligibility-first matching</strong><p>See why a scheme qualifies or does not.</p></div>
        <div><span>02</span><strong>No repeated questions</strong><p>Your location and support amount travel through the flow.</p></div>
        <div><span>03</span><strong>Actionable next step</strong><p>Open scheme details, estimate EMI and find a partner.</p></div>
      </div>
    </div>
  );
}
export default Home;
