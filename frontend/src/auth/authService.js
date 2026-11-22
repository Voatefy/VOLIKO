import { apiRequest } from "../services/api";

export async function login(credentials) {
  const tokens = await apiRequest("/token/", {
    method: "POST",
    body: JSON.stringify(credentials),
  });

  localStorage.setItem("voliko_access", tokens.access);
  localStorage.setItem("voliko_refresh", tokens.refresh);

  return tokens;
}

export async function register(userData) {
  return apiRequest("/utilisateurs/inscription/", {
    method: "POST",
    body: JSON.stringify(userData),
  });
}

export async function getProfile() {
  return apiRequest("/utilisateurs/profil/");
}

export function logout() {
  localStorage.removeItem("voliko_access");
  localStorage.removeItem("voliko_refresh");
}
