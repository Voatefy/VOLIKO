
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
const mapboxToken = import.meta.env.VITE_MAPBOX_TOKEN;

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
          <LayersControl.BaseLayer checked name="Mapbox Satellite">
            <TileLayer
              attribution='© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>'
              url={`https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token=${mapboxToken}`}
              maxZoom={20}
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
