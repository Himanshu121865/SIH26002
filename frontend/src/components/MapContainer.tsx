import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import { Deck } from "@deck.gl/core";
import { HeatmapLayer } from "@deck.gl/aggregation-layers";

const NER_CENTER: [number, number] = [92.5, 25.5];
const NER_ZOOM = 5.5;

interface MapContainerProps {
  showVehicles?: boolean;
  showDisruptions?: boolean;
  showHeatmap?: boolean;
}

function MapContainer({ showVehicles = false, showDisruptions = false, showHeatmap = false }: MapContainerProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const deckRef = useRef<Deck | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: NER_CENTER,
      zoom: NER_ZOOM,
      attributionControl: false,
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    map.on("load", () => {
      map.addSource("ner-roads", {
        type: "geojson",
        data: "/api/v1/routing/roads.geojson",
      });

      map.addLayer({
        id: "ner-roads-line",
        type: "line",
        source: "ner-roads",
        layout: { "line-join": "round", "line-cap": "round" },
        paint: {
          "line-color": "#3b82f6",
          "line-width": 1.5,
          "line-opacity": 0.4,
        },
      });

      if (showVehicles) {
        fetch("/api/v1/tracking/vehicles")
          .then((r) => r.json())
          .then((data) => {
            const vehicles = data.vehicles || [];
            vehicles.forEach((v: any) => {
              const color = v.vehicle_type === "truck" ? "#3b82f6" : v.vehicle_type === "van" ? "#10b981" : "#f59e0b";
              const label = v.vehicle_type === "truck" ? "T" : v.vehicle_type === "van" ? "V" : "K";

              const el = document.createElement("div");
              el.className = "vehicle-marker";
              el.style.cssText = `
                width: 30px; height: 30px; border-radius: 50%;
                background: ${color}; border: 2px solid rgba(255,255,255,0.9);
                cursor: pointer; display: flex; align-items: center; justify-content: center;
                font-size: 11px; color: white; font-weight: 700;
                box-shadow: 0 2px 8px rgba(0,0,0,0.4);
                transition: transform 0.15s;
              `;
              el.textContent = label;
              el.addEventListener("mouseenter", () => { el.style.transform = "scale(1.15)"; });
              el.addEventListener("mouseleave", () => { el.style.transform = "scale(1)"; });

              const popup = new maplibregl.Popup({ offset: 15, closeButton: false }).setHTML(`
                <div class="popup-content">
                  <div class="popup-title">${v.vehicle_id}</div>
                  <div class="popup-subtitle">${v.driver_name}</div>
                  <div class="popup-detail">${v.vehicle_type} — ${v.cargo_type}</div>
                  <div class="popup-detail">${v.speed_kmh} km/h</div>
                  <div class="popup-badge" style="background: ${color}20; color: ${color}">${v.vehicle_type}</div>
                </div>
              `);

              new maplibregl.Marker({ element: el })
                .setLngLat([v.lon, v.lat])
                .setPopup(popup)
                .addTo(map);
            });
          })
          .catch(console.error);
      }

      if (showDisruptions) {
        fetch("/api/v1/routing/disruptions")
          .then((r) => r.json())
          .then((data) => {
            const disruptions = data.disruptions || [];
            disruptions.forEach((d: any) => {
              const color = d.severity === "critical" ? "#ef4444"
                : d.severity === "high" ? "#f97316"
                : d.severity === "moderate" ? "#eab308"
                : "#22c55e";

              const el = document.createElement("div");
              el.style.cssText = `
                width: 18px; height: 18px; border-radius: 50%;
                background: ${color}; border: 2px solid rgba(255,255,255,0.8);
                cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                transition: transform 0.15s;
              `;
              el.addEventListener("mouseenter", () => { el.style.transform = "scale(1.2)"; });
              el.addEventListener("mouseleave", () => { el.style.transform = "scale(1)"; });

              const popup = new maplibregl.Popup({ offset: 15, closeButton: false }).setHTML(`
                <div class="popup-content">
                  <div class="popup-badge" style="background: ${color}20; color: ${color}">${d.severity}</div>
                  <div class="popup-title" style="margin-top: 6px">${d.type.replace(/_/g, " ")}</div>
                  <div class="popup-detail">${d.description}</div>
                </div>
              `);

              new maplibregl.Marker({ element: el })
                .setLngLat([d.lon, d.lat])
                .setPopup(popup)
                .addTo(map);
            });
          })
          .catch(console.error);
      }

      if (showHeatmap) {
        fetch("/api/v1/routing/disruptions")
          .then((r) => r.json())
          .then((data) => {
            const disruptions = data.disruptions || [];
            const points = disruptions
              .filter((d: any) => d.lat > 20 && d.lat < 30 && d.lon > 85 && d.lon < 100)
              .map((d: any) => ({
                coordinates: [d.lon, d.lat],
                weight: d.severity === "critical" ? 3 : d.severity === "high" ? 2 : 1,
              }));

            if (points.length === 0) return;

            deckRef.current = new Deck({
              parent: mapContainer.current!,
              layers: [
                new HeatmapLayer({
                  id: "disruption-heatmap",
                  data: points,
                  getPosition: (d: any) => d.coordinates,
                  getWeight: (d: any) => d.weight,
                  radiusPixels: 60,
                  intensity: 1,
                  threshold: 0.1,
                  colorRange: [
                    [34, 197, 94],
                    [234, 179, 8],
                    [249, 115, 22],
                    [239, 68, 68],
                    [190, 18, 60],
                  ],
                }),
              ],
            });
          })
          .catch(console.error);
      }
    });

    return () => {
      if (deckRef.current) deckRef.current.finalize();
      map.remove();
    };
  }, [showVehicles, showDisruptions, showHeatmap]);

  return <div ref={mapContainer} className="map-container" />;
}

export default MapContainer;
