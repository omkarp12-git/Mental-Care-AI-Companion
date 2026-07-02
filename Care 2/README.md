# Mental Health AI Decision-Support Prototype

This project is a full-stack, runnable prototype for multimodal mental-health risk estimation. It uses a lightweight hybrid demo pipeline by default, so it does not require large DistilBERT, Wav2Vec 2.0, PyTorch, or SHAP downloads to run locally.

The app is a decision-support prototype, not a diagnostic system. Results are risk estimates intended to support reflection and professional follow-up where appropriate.

## Project Structure

```text
backend/      FastAPI API, preprocessing, scoring, explanations, tests
frontend/     React + Vite + Tailwind user interface
datasets/     Placeholder for local datasets
docs/         Architecture and model-extension notes
logs/         Runtime logs
outputs/      Local generated outputs
notebooks/    Research notebooks
```

## Backend Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

API docs will be available at `http://127.0.0.1:8000/docs`.

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000`. Override with `VITE_API_BASE_URL` if needed.

## API Examples

Health:

```powershell
curl http://127.0.0.1:8000/health
```

Text prediction:

```powershell
curl -X POST http://127.0.0.1:8000/predict -F "text=I have felt exhausted and hopeless lately, but I can talk to a friend."
```

Audio and text prediction:

```powershell
curl -X POST http://127.0.0.1:8000/predict -F "text=I feel overwhelmed" -F "audio=@sample.wav"
```

## Testing

```powershell
pytest backend/tests
```

## Model Extension Path

The current implementation keeps the ML layer deterministic and dependency-light. To replace it with real models later, plug DistilBERT into the text preprocessing boundary, Wav2Vec 2.0 into the audio preprocessing boundary, and SHAP into the explanation service. See `docs/model-extension.md`.
