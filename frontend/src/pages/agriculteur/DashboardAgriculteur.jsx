import { useAuth } from "../../auth/AuthContext";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { useEffect, useState } from "react";
import { getParcelles } from "../../services/parcelleService";

function DashboardAgriculteur() {
  const { user } = useAuth();

  const [parcelles, setParcelles] = useState({
    type: "FeatureCollection",
    features: [],
    });

    const [chargement, setChargement] = useState(true);
    const [erreur, setErreur] = useState("");

    useEffect(() => {
    async function chargerParcelles() {
        try {
        const data = await getParcelles();
        setParcelles(data);
        } catch (error) {
        setErreur(error.message);
        } finally {
        setChargement(false);
        }
    }

    chargerParcelles();
    }, []);

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