import { apiRequest } from "./api";

export function getCandidatures(params = {}) {
  const query = new URLSearchParams(params).toString();
  return apiRequest(
    `/collaborations/admin/candidatures/${query ? `?${query}` : ""}`
  );
}

export function traiterCandidature(id, statut, motif_decision = "") {
  return apiRequest(`/collaborations/candidatures/${id}/decision/`, {
    method: "POST",
    body: JSON.stringify({ statut, motif_decision }),
  });
}

export function getDocumentUrl(id) {
  return `${import.meta.env.VITE_API_URL}/collaborations/documents/${id}/telecharger/`;
}
