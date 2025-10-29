"use client";

import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";

interface MapPreviewProps {
  geojsonUrl?: string;
}

export function MapPreview({ geojsonUrl }: MapPreviewProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;
    mapInstance.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
      center: [-93.0, 30.0],
      zoom: 4
    });

    const map = mapInstance.current;

    map.on("load", () => {
      const isRemote = geojsonUrl?.startsWith("http");
      const sourceUrl = isRemote ? geojsonUrl : "/offline/sample.geojson";
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
    });

    return () => {
      mapInstance.current?.remove();
    };
  }, [geojsonUrl]);

  return <div ref={mapContainer} style={{ height: "400px", borderRadius: "16px", overflow: "hidden" }} />;
}
