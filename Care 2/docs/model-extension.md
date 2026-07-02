# Replacing the Hybrid Demo ML Layer

The demo pipeline is split along the same boundaries a real model pipeline would use.

## DistilBERT Text Features

Replace `backend/app/preprocessing/text.py` with a tokenizer/model-backed extractor that returns a fixed-size embedding and risk-relevant metadata. Keep `clean_text` and the public extractor boundary stable so the API and tests remain easy to adapt.

## Wav2Vec 2.0 Audio Features

Replace `backend/app/preprocessing/audio.py` with an audio loader that converts uploads to mono 16 kHz waveform tensors, runs Wav2Vec 2.0, and returns an embedding plus audio quality metadata.

## Fusion and Classifier

Replace `backend/app/pipelines/fusion.py` and `backend/app/scoring/risk.py` with a PyTorch classifier that consumes text and audio embeddings. Preserve the response schema:

```json
{
  "prediction": "Moderate Risk",
  "score": 58,
  "confidence": 0.82,
  "probabilities": {
    "low": 0.22,
    "moderate": 0.58,
    "high": 0.2
  }
}
```

## SHAP

Use SHAP inside `backend/app/services/explanation_service.py`. Keep explanations plain-language and avoid exposing raw technical values to end users.

## Safety

Keep decision-support language in place even after real models are added. The application should not claim to diagnose or replace professional evaluation.
