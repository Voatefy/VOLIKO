import { apiRequest } from "./api";

export function getAlertesAgricoles() {
  return apiRequest("/analyses/alertes/");
}