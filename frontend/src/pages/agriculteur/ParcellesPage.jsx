
import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import ParcelleMap from "../../components/parcelles/ParcelleMap";
import { getParcelles } from "../../services/parcelleService";

function ParcellesPage() {
  const [parcelles, setParcelles] = useState({
    type: "FeatureCollection",
    features: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
              <ParcelleMap parcelles={parcelles} />
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
