const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function requestPrediction({ text, audio }) {
  const formData = new FormData();
  if (text.trim()) {
    formData.append("text", text.trim());
  }
  if (audio) {
    formData.append("audio", audio);
  }

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || "Prediction request failed.");
  }
  return payload;
}
