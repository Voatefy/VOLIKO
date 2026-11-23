
import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { getCandidatures } from "../../services/candidatureService";

function CandidaturesPage() {
  const [candidatures, setCandidatures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function chargerCandidatures() {
      try {
        setLoading(true);
        const data = await getCandidatures();
        setCandidatures(data);
      } catch (err) {
        setError(err.message || "Impossible de charger les candidatures.");
      } finally {
        setLoading(false);
      }
    }

    chargerCandidatures();
  }, []);

  return (
    <DashboardLayout>
      <section className="dashboard-welcome">
        <span className="dashboard-welcome-label">
          ADMINISTRATION
        </span>
        <h2>Gestion des candidatures</h2>
        <p>
          Consultez les demandes d'inscription des candidats agronomes.
        </p>
      </section>

      <section className="candidatures-section">
        {loading && <p>Chargement des candidatures...</p>}

        {error && <p className="error-message">{error}</p>}

        {!loading && !error && candidatures.length === 0 && (
          <p>Aucune candidature soumise pour le moment.</p>
        )}

        {!loading && !error && candidatures.length > 0 && (
          <div className="candidatures-list">
            {candidatures.map((candidature) => (
              <article key={candidature.id} className="candidature-card">
                <h3>
                  {candidature.candidat.first_name}{" "}
                  {candidature.candidat.last_name}
                </h3>

                <p>{candidature.candidat.email}</p>
                <p>
                  Statut : {candidature.statut}
                </p>
                <p>
                  Date de candidature :{" "}
                  {new Date(candidature.date_candidature).toLocaleDateString(
                    "fr-FR"
                  )}
                </p>
              </article>
            ))}
          </div>
        )}
      </section>
    </DashboardLayout>
  );
}

export default CandidaturesPage;
