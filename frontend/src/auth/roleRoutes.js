export const ROLE_HOME = {
  AGRICULTEUR: "/agriculteur",
  AGRONOME: "/agronome",
  CANDIDAT_AGRONOME: "/candidat-agronome",
  ADMINISTRATEUR: "/administration",
};

export function getRoleHomePath(role) {
  return ROLE_HOME[role] || "/";
}
