
import { useEffect, useRef, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import ParcelleMap from "../../components/parcelles/ParcelleMap";
import {
  getParcelles,
  creerParcelle,
} from "../../services/parcelleService";

import { rechercherLieu } from "../../services/geocodingService";
import "./ParcellesPage.css";

function ParcellesPage() {
  const [parcelles, setParcelles] = useState({
    type: "FeatureCollection",
    features: [],
  });
  const [parcelleSelectionnee, setParcelleSelectionnee] = useState(null);
  const [geometrieEnCours, setGeometrieEnCours] = useState(null);
  const [coucheEnCours, setCoucheEnCours] = useState(null);
  const [nomParcelle, setNomParcelle] = useState("");
  const [enregistrement, setEnregistrement] = useState(false);
  const [erreurCreation, setErreurCreation] = useState("");
  const selectionEnCours = useRef(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

const [query, setQuery] = useState("");
const [resultats, setResultats] = useState([]);
const [rechercheLoading, setRechercheLoading] = useState(false);
const [erreurRecherche, setErreurRecherche] = useState("");
const [locationRecherche, setLocationRecherche] = useState(null);

  useEffect(() => {
    async function chargerParcelles() {
      try {
        const data = await getParcelles();
        setParcelles(data);

        if (data.features.length > 0) {
          setParcelleSelectionnee(data.features[0].id);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    chargerParcelles();
  }, []);




  useEffect(() => {
    if (selectionEnCours.current) {
      selectionEnCours.current = false;
      return;
    }

    if (query.trim().length < 2) {
      setResultats([]);
      setErreurRecherche("");
      return;
    }

    const timeout = setTimeout(async () => {
      setRechercheLoading(true);
      setErreurRecherche("");

      try {
        const lieux = await rechercherLieu(query.trim());
        setResultats(lieux);

        if (lieux.length === 0) {
          setErreurRecherche("Aucun lieu trouvé à Madagascar.");
        }
      } catch (err) {
        setErreurRecherche(err.message);
      } finally {
        setRechercheLoading(false);
      }
    }, 350);

    return () => clearTimeout(timeout);
  }, [query]);


  function handleGeometryCreated(geometrie, couche) {
    setGeometrieEnCours(geometrie);
    setCoucheEnCours(couche);
    setErreurCreation("");
  }

  function handleAnnulerCreation() {
    coucheEnCours?.remove();

    setGeometrieEnCours(null);
    setCoucheEnCours(null);
    setNomParcelle("");
    setErreurCreation("");
  }

  function handleEffacer() {
    setQuery("");
    setResultats([]);
    setErreurRecherche("");
    setLocationRecherche(null);
  }

  async function handleCreerParcelle(e) {
    e.preventDefault();

    if (!nomParcelle.trim() || !geometrieEnCours) {
      setErreurCreation("Veuillez saisir un nom et dessiner une parcelle.");
      return;
    }

    setEnregistrement(true);
    setErreurCreation("");

    try {
      const nouvelleParcelle = await creerParcelle({
        nom_parcelle: nomParcelle.trim(),
        geometrie: geometrieEnCours,
      });

      const data = await getParcelles();
      setParcelles(data);
      setParcelleSelectionnee(nouvelleParcelle.id);

      coucheEnCours?.remove();

      setGeometrieEnCours(null);
      setCoucheEnCours(null);
      setNomParcelle("");
      setErreurCreation("");

    } catch (err) {
      setErreurCreation(err.message);
    } finally {
      setEnregistrement(false);
    }
  }

  return (
    <DashboardLayout>
      <section className="parcelles-page">
        <div className="parcelles-heading">
          <div>
            <span>GESTION AGRICOLE</span>
            <h2>Mes parcelles</h2>
            <p>Consultez et gérez vos parcelles agricoles.</p>
          </div>

          <strong>
            {parcelles.features.length} parcelle(s)
          </strong>
        </div>

        {loading && <p>Chargement des parcelles...</p>}

        {error && <p className="error-message">{error}</p>}

        {!loading && !error && (
          <>
            <div className="parcelles-map-container">
              

              <div className="recherche-lieu">
                <span className="recherche-icon"></span>

                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Rechercher un lieu à Madagascar..."
                />

                {query && (
                  <button
                    type="button"
                    onClick={handleEffacer}
                    className="recherche-effacer"
                  >
                    ×
                  </button>
                )}

                {rechercheLoading && (
                  <span className="recherche-loading">...</span>
                )}
              </div>

              {erreurRecherche && (
                <p className="error-message">{erreurRecherche}</p>
              )}

              {resultats.length > 0 && (
                <div className="resultats-recherche">
                  {resultats.map((lieu) => (
                    <button
                      type="button"
                      key={lieu.id}
                      onClick={() => {
                        const nomLieu =
                          lieu.properties.full_address ||
                          lieu.properties.name;

                        selectionEnCours.current = true;
                        setQuery(nomLieu);
                        setLocationRecherche(lieu.geometry.coordinates);
                        setResultats([]);
                        setErreurRecherche("");
                      }}
                    >
                      {lieu.properties.full_address ||
                        lieu.properties.name}
                    </button>
                  ))}
                </div>
              )}

              <ParcelleMap
                parcelles={parcelles}
                locationRecherche={locationRecherche}
                onGeometryCreated={handleGeometryCreated}
                selectedParcelleId={parcelleSelectionnee}
              />



              {geometrieEnCours && (
                <form className="creation-parcelle-form" onSubmit={handleCreerParcelle}>
                  <h3>Nouvelle parcelle</h3>

                  <label htmlFor="nom-parcelle">Nom de la parcelle</label>

                  <input
                    id="nom-parcelle"
                    type="text"
                    value={nomParcelle}
                    onChange={(e) => setNomParcelle(e.target.value)}
                    placeholder="Ex. Parcelle Nord"
                    maxLength={150}
                    required
                  />

                  {erreurCreation && (
                    <p className="error-message">{erreurCreation}</p>
                  )}

                  <div className="creation-parcelle-actions">
                    <button
                      type="button"
                      onClick={handleAnnulerCreation}
                      disabled={enregistrement}
                    >
                      Annuler
                    </button>

                    <button type="submit" disabled={enregistrement}>
                      {enregistrement ? "Enregistrement..." : "Enregistrer la parcelle"}
                    </button>
                  </div>
                </form>
              )}



            </div>

            <div className="parcelles-list">
              <h3>Liste de mes parcelles</h3>

              {parcelles.features.length === 0 ? (
                <p>Aucune parcelle enregistrée pour le moment.</p>
              ) : (
                parcelles.features.map((feature) => (
                  <article
                    key={feature.id}
                    className={
                      String(parcelleSelectionnee) === String(feature.id)
                        ? "parcelle-item selected"
                        : "parcelle-item"
                    }
                    onClick={() =>
                      setParcelleSelectionnee(feature.id)
                    }
                  >
                    <h4>{feature.properties.nom_parcelle}</h4>
                    <p>
                      Superficie :{" "}
                      {Number(feature.properties.superficie).toLocaleString(
                        "fr-FR"
                      )}{" "}
                      m²
                    </p>
                  </article>
                ))
              )}
            </div>
          </>
        )}
      </section>
    </DashboardLayout>
  );
}

export default ParcellesPage;
