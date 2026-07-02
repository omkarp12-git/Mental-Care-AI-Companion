# Architecture

The prototype follows the planned multimodal flow:

```text
Text input       Audio input
    |                |
Text features    Audio features
    |                |
    +----- Fusion ---+
            |
      Risk scoring
            |
 Plain-language explanation
            |
      FastAPI response
            |
       React interface
```

The current ML implementation is deterministic and lightweight. It is intentionally shaped like a production ML pipeline, but it avoids heavyweight model downloads during the first runnable version.

## Backend Responsibilities

- Validate user input and uploaded audio.
- Extract text and audio signals.
- Fuse available modalities.
- Produce probabilities, score, category, confidence, and explanations.
- Log request IDs, timing, model version, and failures without storing raw user content.

## Frontend Responsibilities

- Collect optional text and optional audio.
- Prevent empty submissions.
- Show loading, success, and error states.
- Present results as decision-support estimates, not diagnoses.
