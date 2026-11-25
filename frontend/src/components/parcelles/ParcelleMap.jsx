
import { useEffect, useMemo } from "react";

import {
  MapContainer,
  TileLayer,
  GeoJSON,
  useMap,
  LayersControl,
  LayerGroup,
  Circle,
  CircleMarker,
} from "react-leaflet";


import "leaflet/dist/leaflet.css";
import "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";
import "@geoman-io/leaflet-geoman-free";
const mapboxToken = import.meta.env.VITE_MAPBOX_TOKEN;


function MapNavigation({ location }) {
  const map = useMap();

  useEffect(() => {
    if (location) {
      const [longitude, latitude] = location;

      map.flyTo([latitude, longitude], 16, {
        duration: 1.5,
      });
    } else {
      map.flyTo([-18.8792, 47.5079], 6, {
        duration: 1.5,
      });
    }
  }, [map, location]);

  return null;
}



function MapDrawControl({ onGeometryCreated }) {
  const map = useMap();

  useEffect(() => {
    map.pm.addControls({
      position: "topright",
      drawMarker: false,
      drawCircle: false,
      drawCircleMarker: false,
      drawPolyline: false,
      drawRectangle: false,
      drawPolygon: true,
      editMode: false,
      dragMode: false,
      cutPolygon: false,
      removalMode: false,
      rotateMode: false,
    });

    const handleCreate = (event) => {
      const geometry = event.layer.toGeoJSON().geometry;

      const multiPolygon =
        geometry.type === "Polygon"
          ? {
              type: "MultiPolygon",
              coordinates: [geometry.coordinates],
            }
          : geometry;


          onGeometryCreated?.(multiPolygon, event.layer);
    };

    map.on("pm:create", handleCreate);

    return () => {
      map.off("pm:create", handleCreate);
      map.pm.removeControls();
    };
  }, [map, onGeometryCreated]);

  return null;
}

function RechercheMarker({ location }) {
  if (!location) return null;

  const [longitude, latitude] = location;
  const position = [latitude, longitude];

  return (
    <>
      <Circle
        center={position}
        radius={400}
        pathOptions={{
          color: "#f47721",
          fillColor: "#f47721",
          fillOpacity: 0.12,
          weight: 2,
        }}
      />

      <CircleMarker
        center={position}
        radius={9}
        pathOptions={{
          color: "#ffffff",
          weight: 3,
          fillColor: "#f47721",
          fillOpacity: 1,
        }}
      />
    </>
  );
}



function ParcelleMap({
  parcelles,
  onGeometryCreated,
  locationRecherche,
}) {
  const geojson = useMemo(
    () => parcelles || { type: "FeatureCollection", features: [] },
    [parcelles]
  );

  return (
      <div className="parcelle-map">
      <MapContainer
        center={[-18.8792, 47.5079]}
        zoom={6}
        scrollWheelZoom
        style={{ height: "500px", width: "100%" }}
      >
      <MapNavigation location={locationRecherche} />
      <RechercheMarker location={locationRecherche} />


        <LayersControl position="topleft">
          <LayersControl.BaseLayer name="Esri Satellite + rues">
            <LayerGroup>
              <TileLayer
                attribution="Tiles © Esri, Maxar, Earthstar Geographics"
                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                maxZoom={19}
              />

              <TileLayer
                attribution="© Esri, HERE, Garmin, © OpenStreetMap contributors"
                url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
                maxZoom={19}
              />

              <TileLayer
                attribution="© Esri, HERE, Garmin"
                url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}"
                maxZoom={19}
              />
            </LayerGroup>
          </LayersControl.BaseLayer>

          <LayersControl.BaseLayer checked name="Mapbox Satellite + rues">
            <TileLayer
              attribution='© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>'
              url={`https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/256/{z}/{x}/{y}?access_token=${mapboxToken}`}
              maxZoom={20}
            />
          </LayersControl.BaseLayer>

          <LayersControl.BaseLayer name="Carte classique">
            <TileLayer
              attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
          </LayersControl.BaseLayer>
        </LayersControl>


        <GeoJSON data={geojson} />

        <MapDrawControl onGeometryCreated={onGeometryCreated} />
      </MapContainer>
    </div>
  );
}

export default ParcelleMap;
