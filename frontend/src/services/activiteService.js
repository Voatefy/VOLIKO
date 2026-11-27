import { apiRequest } from "./api";

export function getActivitesPlanifiees() {
  return apiRequest("/activites/");
}

export function getActivitesRealisees() {
  return apiRequest("/activites/realisees/");
}