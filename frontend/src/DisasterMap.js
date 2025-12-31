import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix Leaflet marker issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function DisasterMap() {
  const [disasters, setDisasters] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/disasters")
      .then((res) => {
        setDisasters(res.data);
      })
      .catch((err) => {
        console.error("Error fetching disasters:", err);
      });
  }, []);

  return (
    <MapContainer
      center={[20.5937, 78.9629]} // India center
      zoom={5}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {disasters.map((d) => (
        <Marker key={d.id} position={[d.latitude, d.longitude]}>
          <Popup>
            <b>Type:</b> {d.disaster_type} <br />
            <b>Risk:</b> {d.risk_level} <br />
            <b>Severity:</b> {d.severity_score}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default DisasterMap;
