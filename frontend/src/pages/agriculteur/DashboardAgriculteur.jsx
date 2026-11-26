import { useAuth } from "../../auth/AuthContext";
import DashboardLayout from "../../components/layout/DashboardLayout";

function DashboardAgriculteur() {
  const { user } = useAuth();

  return (
    <DashboardLayout>
      <section className="dashboard-welcome">
        <span className="dashboard-welcome-label">
          BIENVENUE SUR VOLIKO
        </span>

        <h2>
          Bonjour {user?.first_name || "Agriculteur"} !
        </h2>

        <p>
          Retrouvez ici une vue d'ensemble de votre exploitation agricole.
        </p>
      </section>
    </DashboardLayout>
  );
}

export default DashboardAgriculteur;