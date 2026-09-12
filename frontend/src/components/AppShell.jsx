import { NavLink, useLocation } from "react-router-dom";
import logo from "../assets/nitinexus-logo.png";

const navItems = [
  { to: "/", label: "Overview", icon: "⌂" },
  { to: "/profile", label: "Find Schemes", icon: "⌕" },
  { to: "/dashboard", label: "Recommendations", icon: "◈" },
  { to: "/partners", label: "Channel Partners", icon: "⌖" },
  { to: "/faq", label: "FAQ", icon: "?" },
];

function AppShell({ children }) {
  const { pathname } = useLocation();
  const isActiveFlow = pathname !== "/";

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="brand-block brand-block-logo">
          <img className="brand-logo" src={logo} alt="NitiNexus" />
          <span className="brand-program">SIH 26092 · SCHEME DISCOVERY</span>
        </div>

        <nav className="sidebar-nav" aria-label="Main navigation">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `sidebar-link ${isActive ? "active" : ""}`}
            >
              <span className="sidebar-icon">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span className="online-dot" />
          <div>
            <strong>Matching engine online</strong>
            <small>Scheme data ready</small>
          </div>
        </div>
      </aside>

      <main className="app-main">
        <header className="topbar">
          <div className="topbar-status"><span className="online-dot" /> Service online</div>
          <div className="topbar-right">
            <span className="topbar-label">Government Scheme Discovery</span>
            <span className="topbar-chip">{isActiveFlow ? "LIVE" : "READY"}</span>
          </div>
        </header>
        <div className="app-content">{children}</div>
      </main>
    </div>
  );
}

export default AppShell;
