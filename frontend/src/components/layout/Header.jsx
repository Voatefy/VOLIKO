import { useLocation } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";

const pageTitles = {
  "/agriculteur": "Tableau de bord",
  "/agronome": "Tableau de bord",
  "/candidat-agronome": "Tableau de bord",
  "/administration": "Tableau de bord",
};

function Header() {
  const { user } = useAuth();
  const location = useLocation();

  const title =
    pageTitles[location.pathname] ||
    location.pathname.split("/").filter(Boolean).pop()
      ?.replaceAll("-", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase()) ||
    "Tableau de bord";

  return (
    <header className="dashboard-header">
      <div>
        <span className="header-eyebrow">VOLIKO / ESPACE DE TRAVAIL</span>
        <h1>{title}</h1>
      </div>

      <div className="header-profile">
        <span>{user?.first_name || user?.username}</span>
        <div className="header-avatar">
          {(user?.first_name || user?.username || "U")
            .charAt(0)
            .toUpperCase()}
        </div>
      </div>
    </header>
  );
}

export default Header;
