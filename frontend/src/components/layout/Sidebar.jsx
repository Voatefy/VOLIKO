import { NavLink } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import volikoLeaf from "../../assets/voliko-leaf.png";

const menus = {
  AGRICULTEUR: [
    { label: "Tableau de bord", path: "/agriculteur" },
    { label: "Mes parcelles", path: "/agriculteur/parcelles" },
    { label: "Activités agricoles", path: "/agriculteur/activites" },
    { label: "Analyses", path: "/agriculteur/analyses" },
    { label: "Alertes", path: "/agriculteur/alertes" },
    { label: "Conseils", path: "/agriculteur/conseils" },
    { label: "Collaborations", path: "/agriculteur/collaborations" },
    { label: "Notifications", path: "/agriculteur/notifications" },
  ],
  AGRONOME: [
    { label: "Tableau de bord", path: "/agronome" },
    { label: "Parcelles accessibles", path: "/agronome/parcelles" },
    { label: "Activités agricoles", path: "/agronome/activites" },
    { label: "Analyses", path: "/agronome/analyses" },
    { label: "Autorisations", path: "/agronome/autorisations" },
    { label: "Notifications", path: "/agronome/notifications" },
  ],
  CANDIDAT_AGRONOME: [
    { label: "Tableau de bord", path: "/candidat-agronome" },
    { label: "Ma candidature", path: "/candidat-agronome/candidature" },
    { label: "Mes documents", path: "/candidat-agronome/documents" },
    { label: "Notifications", path: "/candidat-agronome/notifications" },
  ],
  ADMINISTRATEUR: [
    { label: "Tableau de bord", path: "/administration" },
    { label: "Candidatures", path: "/administration/candidatures" },
  ],
};

function Sidebar() {
  const { user, logout } = useAuth();
  const items = menus[user?.role] || [];

  return (
    <aside className="dashboard-sidebar">
      <NavLink to="/" className="dashboard-brand">
        <img src={volikoLeaf} alt="" />
        <span>Voliko</span>
      </NavLink>

      <div className="sidebar-section-label">ESPACE DE TRAVAIL</div>

      <nav className="sidebar-nav">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === `/${user?.role === "ADMINISTRATEUR" ? "administration" : user?.role === "CANDIDAT_AGRONOME" ? "candidat-agronome" : user?.role?.toLowerCase()}`}
            className={({ isActive }) =>
              `sidebar-link${isActive ? " active" : ""}`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="sidebar-user">
          <div className="sidebar-avatar">
            {(user?.first_name || user?.username || "U").charAt(0).toUpperCase()}
          </div>
          <div className="sidebar-user-info">
            <strong>{user?.first_name || user?.username}</strong>
            <span>{user?.role?.replaceAll("_", " ")}</span>
          </div>
        </div>

        <button className="sidebar-logout" onClick={logout}>
          Se déconnecter
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
