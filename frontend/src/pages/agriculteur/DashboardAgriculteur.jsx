import { useAuth } from "../../auth/AuthContext";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { useEffect, useState } from "react";
import { getParcelles } from "../../services/parcelleService";
import { getActivitesPlanifiees } from "../../services/activiteService";
import { getAlertesAgricoles } from "../../services/analyseService";

function DashboardAgriculteur() {
  const { user } = useAuth();

  const [parcelles, setParcelles] = useState({
    type: "FeatureCollection",
    features: [],
    });

    const [chargement, setChargement] = useState(true);
    const [erreur, setErreur] = useState("");
    const [activites, setActivites] = useState([]);
    const [erreurActivites, setErreurActivites] = useState("");
    const [alertes, setAlertes] = useState([]);
    const [erreurAlertes, setErreurAlertes] = useState("");

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

    useEffect(() => {
      async function chargerActivites() {
        try {
          const data = await getActivitesPlanifiees();
          setActivites(data);
        } catch (error) {
          setErreurActivites(error.message);
        }
      }

      chargerActivites();
    }, []);


    useEffect(() => {
      async function chargerAlertes() {
        try {
          const data = await getAlertesAgricoles();
          setAlertes(data);
        } catch (error) {
          setErreurAlertes(error.message);
        }
      }

      chargerAlertes();
    }, []);

    const nombreAlertes = alertes.length;
    const nombreActivitesPlanifiees = activites.filter(
      (activite) => activite.statut === "PLANIFIEE"
    ).length;

    const nombreParcelles = parcelles.features.length;

    const superficieTotale = parcelles.features.reduce(
      (total, parcelle) => total + Number(parcelle.properties.superficie || 0),
      0
    );

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

      {chargement ? (
        <p>Chargement des indicateurs...</p>
      ) : erreur ? (
        <p>Erreur : {erreur}</p>
      ) : (
        <div className="dashboard-stats">
          <article className="dashboard-stat-card">
            <span>Parcelles actives</span>
            <strong>{nombreParcelles}</strong>
          </article>

          <article className="dashboard-stat-card">
            <span>Superficie totale</span>
            <strong>
              {(superficieTotale / 10000).toFixed(2)} ha
            </strong>
          </article>

          <article className="dashboard-stat-card">
            <span>Activités planifiées</span>
            <strong>
              {erreurActivites ? "—" : nombreActivitesPlanifiees}
            </strong>
            {erreurActivites && (
              <small>Erreur : {erreurActivites}</small>
            )}
          </article>

          <article className="dashboard-stat-card">
            <span>Alertes agricoles</span>
            <strong>
              {erreurAlertes ? "—" : nombreAlertes}
            </strong>
            {erreurAlertes && (
              <small>Erreur : {erreurAlertes}</small>
            )}
          </article>

        </div>
      )}
    </DashboardLayout>
  );
}

export default DashboardAgriculteur;