
import { useEffect, useMemo } from "react";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  useMap,
  LayersControl,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css";
import "@geoman-io/leaflet-geoman-free";

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

      onGeometryCreated?.(multiPolygon);
    };

    map.on("pm:create", handleCreate);

    return () => {
      map.off("pm:create", handleCreate);
      map.pm.removeControls();
    };
  }, [map, onGeometryCreated]);

  return null;
}

function ParcelleMap({ parcelles, onGeometryCreated }) {
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
        <LayersControl position="topleft">
          <LayersControl.BaseLayer checked name="Satellite">
            <TileLayer
              attribution="Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics"
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            />
          </LayersControl.BaseLayer>

          <LayersControl.BaseLayer name="Carte classique">
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
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
