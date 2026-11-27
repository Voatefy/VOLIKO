import { apiRequest } from "./api";

export function getActivitesPlanifiees() {
  return apiRequest("/activites/");
}