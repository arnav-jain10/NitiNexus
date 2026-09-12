import { useLocation, useNavigate } from "react-router-dom";

const FLOW = {
  "/": { back: null, next: "/profile", nextLabel: "Start" },
  "/profile": { back: "/", next: "/dashboard", nextLabel: "Next: Results" },
  "/dashboard": { back: "/profile", next: "/scheme-details", nextLabel: "Next: Scheme Details" },
  "/scheme-details": { back: "/dashboard", next: "/partners", nextLabel: "Next: Partners" },
  "/SchemeDetails": { back: "/dashboard", next: "/partners", nextLabel: "Next: Partners" },
  "/partners": { back: "/scheme-details", next: "/", nextLabel: "Finish" },
  "/partner-details": { back: "/partners", next: "/", nextLabel: "Finish" },
  "/PartnerDetails": { back: "/partners", next: "/", nextLabel: "Finish" },
};

function PageNavigation({ backTo, nextTo, nextLabel, onNext, nextDisabled = false }) {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const defaults = FLOW[pathname] || { back: "/", next: "/", nextLabel: "Next" };
  const backPath = backTo ?? defaults.back;
  const nextPath = nextTo ?? defaults.next;
  const label = nextLabel ?? defaults.nextLabel;

  return (
    <div className="page-navigation" aria-label="Page navigation">
      {backPath ? (
        <button type="button" className="page-nav-button page-nav-back" onClick={() => navigate(backPath)}>
          ← Back
        </button>
      ) : <span />}
      <button
        type="button"
        className="page-nav-button page-nav-next"
        onClick={() => (onNext ? onNext() : nextPath && navigate(nextPath))}
        disabled={nextDisabled || !nextPath}
      >
        {label} →
      </button>
    </div>
  );
}

export default PageNavigation;
