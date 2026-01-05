"use client";

import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";

interface MapPreviewProps {
  geojsonUrl?: string;
  className?: string;
}

export function MapPreview({ geojsonUrl, className }: MapPreviewProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapContainer.current || mapInstance.current) return;
    mapInstance.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
      center: [-93.0, 30.0],
      zoom: 4
    });

    return () => {
      mapInstance.current?.remove();
      mapInstance.current = null;
    };
  }, []);

  useEffect(() => {
    const map = mapInstance.current;
    if (!map) return;

    const sourceUrl = geojsonUrl ?? "/offline/sample.geojson";
    const updateSource = () => {
      const existing = map.getSource("hazards") as maplibregl.GeoJSONSource | undefined;
      if (existing) {
        existing.setData(sourceUrl);
        return;
      }
      map.addSource("hazards", {
        type: "geojson",
        data: sourceUrl
      });
      map.addLayer({
        id: "hazard-points",
        type: "circle",
        source: "hazards",
        paint: {
          "circle-radius": 6,
          "circle-color": [
            "match",
            ["get", "hazard"],
            "hurricane",
            "#f97316",
            "flood",
            "#2563eb",
            "wildfire",
            "#dc2626",
            "#6366f1"
          ],
          "circle-stroke-width": 1,
          "circle-stroke-color": "#ffffff"
        }
      });
    };

    if (map.isStyleLoaded()) {
      updateSource();
      return;
    }
    map.once("load", updateSource);
  }, [geojsonUrl]);

  return <div ref={mapContainer} className={className ?? "map-canvas"} />;
}
