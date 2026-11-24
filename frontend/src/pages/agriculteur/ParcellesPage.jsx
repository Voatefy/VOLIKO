
import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import ParcelleMap from "../../components/parcelles/ParcelleMap";
import { getParcelles } from "../../services/parcelleService";
import { rechercherLieu } from "../../services/geocodingService";
import "./ParcellesPage.css";

function ParcellesPage() {
  const [parcelles, setParcelles] = useState({
    type: "FeatureCollection",
    features: [],
  });
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
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    chargerParcelles();
  }, []);



  async function handleRecherche(event) {
    event.preventDefault();

    if (!query.trim()) return;

    setRechercheLoading(true);
    setErreurRecherche("");
    setResultats([]);

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
              <form onSubmit={handleRecherche} className="recherche-lieu">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Rechercher une région, commune, fokontany, village..."
                />

                <button type="submit" disabled={rechercheLoading}>
                  {rechercheLoading ? "Recherche..." : "Rechercher"}
                </button>
              </form>

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
              />
            </div>

            <div className="parcelles-list">
              <h3>Liste de mes parcelles</h3>

              {parcelles.features.length === 0 ? (
                <p>Aucune parcelle enregistrée pour le moment.</p>
              ) : (
                parcelles.features.map((feature) => (
                  <article key={feature.properties.id}>
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
