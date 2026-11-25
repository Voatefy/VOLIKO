const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

export async function rechercherLieu(query) {
  if (!MAPBOX_TOKEN) {
    throw new Error("Token Mapbox introuvable.");
  }

  const params = new URLSearchParams({
    q: query,
    access_token: MAPBOX_TOKEN,
    country: "MG",
    language: "fr",
    limit: "6",
    autocomplete: "true",
    types: "region,district,place,locality,neighborhood,street,address",
  });

  const response = await fetch(
    `https://api.mapbox.com/search/geocode/v6/forward?${params}`
  );

  if (!response.ok) {
    throw new Error("La recherche géographique a échoué.");
  }

  const data = await response.json();

  return data.features || [];
}
