
import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import {
  getCandidatures,
  getDocumentsCandidature,
  getDocumentUrl,
  traiterCandidature,
} from "../../services/candidatureService";

function CandidaturesPage() {
  const [candidatures, setCandidatures] = useState([]);
  const [documents, setDocuments] = useState({});
  const [documentsOuverts, setDocumentsOuverts] = useState({});
  const [loading, setLoading] = useState(true);
  const [loadingDocuments, setLoadingDocuments] = useState({});
  const [error, setError] = useState("");
  const [documentError, setDocumentError] = useState({});
  const [decision, setDecision] = useState(null);
  const [motif, setMotif] = useState("");
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState("");

  async function chargerCandidatures() {
    try {
      setLoading(true);
      const data = await getCandidatures();
      setCandidatures(data);
      setError("");
    } catch (err) {
      setError(err.message || "Impossible de charger les candidatures.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    chargerCandidatures();
  }, []);

  async function afficherDocuments(id) {
    const estOuvert = documentsOuverts[id];

    setDocumentsOuverts((prev) => ({
      ...prev,
      [id]: !estOuvert,
    }));

    if (estOuvert || documents[id]) return;

    try {
      setLoadingDocuments((prev) => ({ ...prev, [id]: true }));

      const data = await getDocumentsCandidature(id);

      setDocuments((prev) => ({ ...prev, [id]: data }));
    } catch (err) {
      setDocumentError((prev) => ({ ...prev, [id]: err.message }));
    } finally {
      setLoadingDocuments((prev) => ({ ...prev, [id]: false }));
    }
  }

  async function telechargerDocument(doc) {
    try {
      const token = localStorage.getItem("voliko_access");

      const response = await fetch(getDocumentUrl(doc.id), {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        throw new Error("Impossible de télécharger ce document.");
      }

      const fichier = await response.blob();
      const url = URL.createObjectURL(fichier);
      const lien = document.createElement("a");

      lien.href = url;
      lien.download = doc.nom_fichier;
      document.body.appendChild(lien);
      lien.click();
      lien.remove();

      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (err) {
      alert(err.message);
    }
  }

  function ouvrirDecision(candidature, statut) {
    setDecision({ id: candidature.id, statut });
    setMotif("");
    setActionError("");
  }

  async function confirmerDecision() {
    if (!decision) return;

    if (decision.statut === "REJETEE" && !motif.trim()) {
      setActionError("Le motif du refus est obligatoire.");
      return;
    }

    try {
      setActionLoading(true);
      setActionError("");

      await traiterCandidature(
        decision.id,
        decision.statut,
        motif.trim()
      );

      setDecision(null);
      setMotif("");

      await chargerCandidatures();
    } catch (err) {
      setActionError(
        err.message || "Impossible de traiter cette candidature."
      );
    } finally {
      setActionLoading(false);
    }
  }

  return (
    <DashboardLayout>
      <section className="dashboard-welcome">
        <span className="dashboard-welcome-label">
          ADMINISTRATION
        </span>
        <h2>Gestion des candidatures</h2>
        <p>
          Consultez et traitez les demandes d'inscription des candidats agronomes.
        </p>
      </section>

      <section className="candidatures-section">
        {loading && <p>Chargement des candidatures...</p>}
        {error && <p>{error}</p>}

        {!loading && !error && candidatures.length === 0 && (
          <p>Aucune candidature soumise pour le moment.</p>
        )}

        {!loading && !error && candidatures.map((candidature) => {
          const candidat = candidature.candidat || {};
          const nom = [
            candidat.first_name,
            candidat.last_name,
          ].filter(Boolean).join(" ");

          const enAttente = [
            "SOUMISE",
            "EN_EXAMEN",
          ].includes(candidature.statut);

          return (
            <article key={candidature.id} className="candidature-card">
              <h3>{nom || candidat.username || "Candidat sans nom"}</h3>

              <p>{candidat.email || "Adresse e-mail non renseignée"}</p>
              <p>Statut : {candidature.statut}</p>

              <p>
                Date de candidature :{" "}
                {new Date(candidature.date_candidature).toLocaleDateString("fr-FR")}
              </p>

              {candidature.motif_decision && (
                <p>Motif de décision : {candidature.motif_decision}</p>
              )}

              <button
                type="button"
                onClick={() => afficherDocuments(candidature.id)}
              >
                {documentsOuverts[candidature.id]
                  ? "Masquer les documents"
                  : "Consulter les documents"}
              </button>

              {documentsOuverts[candidature.id] && (
                <div className="documents-list">
                  {loadingDocuments[candidature.id] && (
                    <p>Chargement des documents...</p>
                  )}

                  {documentError[candidature.id] && (
                    <p>{documentError[candidature.id]}</p>
                  )}

                  {!loadingDocuments[candidature.id] &&
                    !documentError[candidature.id] &&
                    documents[candidature.id]?.length === 0 && (
                      <p>Aucun document fourni.</p>
                    )}

                  {documents[candidature.id]?.map((doc) => (
                    <div key={doc.id} className="document-item">
                      <span>
                        {doc.nom_fichier} ({doc.type_document})
                      </span>

                      <button
                        type="button"
                        onClick={() => telechargerDocument(doc)}
                      >
                        Télécharger
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {enAttente && (
                <div className="candidature-actions">
                  <button
                    type="button"
                    disabled={actionLoading}
                    onClick={() => ouvrirDecision(candidature, "ACCEPTEE")}
                  >
                    Accepter
                  </button>

                  <button
                    type="button"
                    disabled={actionLoading}
                    onClick={() => ouvrirDecision(candidature, "REJETEE")}
                  >
                    Refuser
                  </button>
                </div>
              )}
            </article>
          );
        })}
      </section>

      {decision && (
        <section className="decision-panel">
          <h3>
            {decision.statut === "ACCEPTEE"
              ? "Confirmer l'acceptation"
              : "Refuser la candidature"}
          </h3>

          {decision.statut === "ACCEPTEE" ? (
            <p>
              Confirmer l'acceptation de cette candidature ?
              Le rôle du candidat deviendra AGRONOME.
            </p>
          ) : (
            <>
              <label htmlFor="motif-decision">
                Motif du refus (obligatoire)
              </label>

              <textarea
                id="motif-decision"
                value={motif}
                onChange={(e) => setMotif(e.target.value)}
                placeholder="Indiquez le motif du refus..."
                rows={4}
              />
            </>
          )}

          {actionError && <p>{actionError}</p>}

          <button
            type="button"
            disabled={actionLoading}
            onClick={confirmerDecision}
          >
            {actionLoading ? "Traitement..." : "Confirmer"}
          </button>

          <button
            type="button"
            disabled={actionLoading}
            onClick={() => setDecision(null)}
          >
            Annuler
          </button>
        </section>
      )}
    </DashboardLayout>
  );
}

export default CandidaturesPage;
