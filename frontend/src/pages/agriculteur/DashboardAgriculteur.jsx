import { useAuth } from "../../auth/AuthContext";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { useEffect, useId, useState } from "react";
import { getParcelles } from "../../services/parcelleService";
import {
  getActivitesPlanifiees,
  getActivitesRealisees,
} from "../../services/activiteService";

import { getAlertesAgricoles } from "../../services/analyseService";
import {
  Map,
  Ruler,
  CalendarDays,
  AlertTriangle,
  ChevronDown,
} from "lucide-react";

function formaterTypeActivite(type) {
  const types = {
    SEMIS: "Semis",
    IRRIGATION: "Irrigation",
    FERTILISATION: "Fertilisation",
    TRAITEMENT: "Traitement",
    RECOLTE: "Récolte",
    AUTRE: "Autre",
  };

  return types[type] || type;
}

function formaterDate(date) {
  if (!date) return "Date non disponible";

  return new Date(date).toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
}

function formaterTypeAlerte(type) {
  const types = {
    VEGETATION: "Végétation",
    METEO: "Météo",
    AUTRE: "Autre",
  };

  return types[type] || type;
}

function formaterNiveauAlerte(niveau) {
  const niveaux = {
    FAIBLE: "Faible",
    MOYEN: "Moyen",
    ELEVE: "Élevé",
    CRITIQUE: "Critique",
  };

  return niveaux[niveau] || niveau;
}

/* ---------------------------------------------------------
   Section repliable animée.
   Le contenu reste TOUJOURS dans le DOM : c'est la classe
   "is-open" qui anime l'ouverture et la fermeture.
--------------------------------------------------------- */

function SectionRepliable({
  titre,
  nombre = 0,
  variante,
  ouverte,
  onToggle,
  children,
}) {
  const contenuId = useId();

  return (
    <section className="dashboard-recent">
      <button
        className="dashboard-recent-toggle"
        onClick={onToggle}
        aria-expanded={ouverte}
        aria-controls={contenuId}
        type="button"
      >
        <h3>
          {titre}
          {nombre > 0 && (
            <span
              className={`recent-count${
                variante === "alerte" ? " recent-count--alert" : ""
              }`}
            >
              {nombre}
            </span>
          )}
        </h3>
        <ChevronDown className={ouverte ? "chevron-open" : ""} size={22} />
      </button>

      <div
        id={contenuId}
        className={`recent-collapse${ouverte ? " is-open" : ""}`}
      >
        <div className="recent-collapse-inner">{children}</div>
      </div>
    </section>
  );
}

function DashboardAgriculteur() {
  const { user } = useAuth();
  const [activitesOuvertes, setActivitesOuvertes] = useState(true);
  const [alertesOuvertes, setAlertesOuvertes] = useState(true);

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
  const [activitesRealisees, setActivitesRealisees] = useState([]);
  const [erreurActivitesRealisees, setErreurActivitesRealisees] = useState("");

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
    async function chargerActivitesRealisees() {
      try {
        const data = await getActivitesRealisees();
        setActivitesRealisees(data);
      } catch (error) {
        setErreurActivitesRealisees(error.message);
      }
    }

    chargerActivitesRealisees();
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
  const alertesRecentes = [...alertes]
    .sort((a, b) => new Date(b.date_alerte) - new Date(a.date_alerte))
    .slice(0, 5);

  const activitesRecentes = [...activitesRealisees]
    .sort((a, b) => new Date(b.date_activite) - new Date(a.date_activite))
    .slice(0, 5);

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
        <p className="dashboard-welcome-eyebrow">Bienvenue sur Voliko</p>

        <h2>Bonjour {user?.first_name || "Agriculteur"} !</h2>

        <p>Retrouvez ici une vue d'ensemble de votre exploitation agricole.</p>
      </section>

      {chargement ? (
        <p>Chargement des indicateurs...</p>
      ) : erreur ? (
        <p>Erreur : {erreur}</p>
      ) : (
        <>
          <div className="dashboard-stats">
            <article className="dashboard-stat-card">
              <div className="dashboard-stat-icon" aria-hidden="true">
                <Map size={24} />
              </div>
              <span>Parcelles actives</span>
              <strong>{nombreParcelles}</strong>
            </article>

            <article className="dashboard-stat-card">
              <div className="dashboard-stat-icon" aria-hidden="true">
                <Ruler size={24} />
              </div>
              <span>Superficie totale</span>
              <strong>{(superficieTotale / 10000).toFixed(2)} ha</strong>
            </article>

            <article className="dashboard-stat-card">
              <div className="dashboard-stat-icon" aria-hidden="true">
                <CalendarDays size={24} />
              </div>
              <span>Activités planifiées</span>
              <strong>
                {erreurActivites ? "—" : nombreActivitesPlanifiees}
              </strong>
              {erreurActivites && <small>Erreur : {erreurActivites}</small>}
            </article>

            <article
              className={`dashboard-stat-card${
                !erreurAlertes && nombreAlertes > 0
                  ? " dashboard-stat-card--alert"
                  : ""
              }`}
            >
              <div className="dashboard-stat-icon" aria-hidden="true">
                <AlertTriangle size={24} />
              </div>
              <span>Alertes agricoles</span>
              <strong>{erreurAlertes ? "—" : nombreAlertes}</strong>
              {erreurAlertes && <small>Erreur : {erreurAlertes}</small>}
            </article>
          </div>

          <SectionRepliable
            titre="Activités agricoles récentes"
            nombre={erreurActivitesRealisees ? 0 : activitesRecentes.length}
            ouverte={activitesOuvertes}
            onToggle={() => setActivitesOuvertes(!activitesOuvertes)}
          >
            {erreurActivitesRealisees ? (
              <p>Erreur : {erreurActivitesRealisees}</p>
            ) : activitesRecentes.length === 0 ? (
              <p>Aucune activité agricole réalisée pour le moment.</p>
            ) : (
              <ul>
                {activitesRecentes.map((activite) => {
                  const parcelleAssociee = parcelles.features.find(
                    (parcelle) => parcelle.id === activite.parcelle
                  );

                  return (
                    <li key={activite.id} className="dashboard-activite-item">
                      <div className="activite-card-header">
                        <strong>
                          {formaterTypeActivite(activite.type_activite)}
                        </strong>

                        <span className="activite-date">
                          <CalendarDays size={15} />
                          {formaterDate(activite.date_activite)}
                        </span>
                      </div>

                      <div className="activite-card-details">
                        <div className="activite-detail">
                          <span className="activite-detail-label">
                            Parcelle
                          </span>
                          <strong className="activite-parcelle">
                            {parcelleAssociee
                              ? parcelleAssociee.properties.nom_parcelle
                              : "Parcelle inconnue"}
                          </strong>
                        </div>

                        {activite.description && (
                          <div className="activite-detail">
                            <span className="activite-detail-label">
                              Description
                            </span>
                            <p>{activite.description}</p>
                          </div>
                        )}

                        {activite.intrant && (
                          <div className="activite-detail">
                            <span className="activite-detail-label">
                              Intrant utilisé
                            </span>
                            <p>{activite.intrant}</p>
                          </div>
                        )}
                      </div>
                    </li>
                  );
                })}
              </ul>
            )}
          </SectionRepliable>

          <SectionRepliable
            titre="Alertes agricoles récentes"
            nombre={erreurAlertes ? 0 : alertesRecentes.length}
            variante="alerte"
            ouverte={alertesOuvertes}
            onToggle={() => setAlertesOuvertes(!alertesOuvertes)}
          >
            {erreurAlertes ? (
              <p>Erreur : {erreurAlertes}</p>
            ) : alertesRecentes.length === 0 ? (
              <p>Aucune alerte agricole pour le moment.</p>
            ) : (
              <ul>
                {alertesRecentes.map((alerte) => {
                  const parcelleAssociee = parcelles.features.find(
                    (parcelle) => parcelle.id === alerte.parcelle
                  );

                  return (
                    <li key={alerte.id} className="dashboard-alert-item">
                      <div className="alerte-card-header">
                        <strong>
                          {formaterTypeAlerte(alerte.type_alerte)}
                        </strong>

                        <span
                          className={`alerte-niveau alerte-niveau-${alerte.niveau_alerte?.toLowerCase()}`}
                        >
                          {formaterNiveauAlerte(alerte.niveau_alerte)}
                        </span>
                      </div>

                      <div className="alerte-card-details">
                        <div className="alerte-detail">
                          <span className="alerte-detail-label">
                            Description de l'alerte
                          </span>
                          <p>{alerte.contenu_alerte}</p>
                        </div>

                        <div className="alerte-detail">
                          <span className="alerte-detail-label">
                            Parcelle concernée
                          </span>
                          <strong className="alerte-parcelle">
                            {parcelleAssociee
                              ? parcelleAssociee.properties.nom_parcelle
                              : "Parcelle inconnue"}
                          </strong>
                        </div>

                        <div className="alerte-date">
                          <CalendarDays size={15} />
                          {formaterDate(alerte.date_alerte)}
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            )}
          </SectionRepliable>
        </>
      )}
    </DashboardLayout>
  );
}

export default DashboardAgriculteur;