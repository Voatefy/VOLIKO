import { apiRequest } from "./api";

export function getParcelles() {
  return apiRequest("/parcelles/");
}

export function getCulturesDisponibles() {
  return apiRequest("/parcelles/cultures-disponibles/");
}

export function creerParcelle(data) {
  return apiRequest("/parcelles/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getParcelle(id) {
  return apiRequest(`/parcelles/${id}/`);
}

export function modifierParcelle(id, data) {
  return apiRequest(`/parcelles/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function supprimerParcelle(id) {
  return apiRequest(`/parcelles/${id}/`, {
    method: "DELETE",
  });
}
