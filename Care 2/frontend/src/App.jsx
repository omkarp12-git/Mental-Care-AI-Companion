import { AlertCircle, AudioLines, Brain, FileAudio, HeartPulse, Loader2, ShieldCheck, Sparkles } from "lucide-react";
import { useMemo, useState } from "react";
import { requestPrediction } from "./services/api";

const categoryStyles = {
  "Low Risk": "bg-emerald-50 text-emerald-800 border-emerald-200",
  "Moderate Risk": "bg-amber-50 text-amber-800 border-amber-200",
  "High Risk": "bg-rose-50 text-rose-800 border-rose-200"
};

function App() {
  const [text, setText] = useState("");
  const [audio, setAudio] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const canSubmit = useMemo(() => text.trim().length > 0 || audio, [text, audio]);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!canSubmit) {
      setError("Add text, upload audio, or provide both before requesting an estimate.");
      return;
    }

    setIsLoading(true);
    try {
      const prediction = await requestPrediction({ text, audio });
      setResult(prediction);
    } catch (requestError) {
      setError(requestError.message || "Unable to connect to the decision-support API.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-5 sm:px-6 lg:px-8">
        <header className="flex items-center justify-between border-b border-slate-200 pb-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-600 text-white">
              <HeartPulse aria-hidden="true" size={24} />
            </div>
            <div>
              <h1 className="text-lg font-semibold tracking-normal text-slate-950 sm:text-xl">
                Mental Health AI Decision Support
              </h1>
              <p className="text-sm text-slate-600">Hybrid multimodal risk estimate</p>
            </div>
          </div>
          <div className="hidden items-center gap-2 rounded-full border border-blue-100 bg-white px-3 py-1 text-sm font-medium text-blue-700 shadow-sm sm:flex">
            <ShieldCheck aria-hidden="true" size={16} />
            Not a diagnosis
          </div>
        </header>

        <section className="grid flex-1 gap-5 py-5 lg:grid-cols-[minmax(0,1fr)_420px]">
          <form onSubmit={handleSubmit} className="flex min-h-[620px] flex-col gap-5 rounded-lg border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex items-center gap-2 text-blue-700">
              <Brain aria-hidden="true" size={20} />
              <h2 className="text-base font-semibold text-slate-950">Assessment Inputs</h2>
            </div>

            <label className="flex flex-1 flex-col gap-2">
              <span className="text-sm font-medium text-slate-800">Text input</span>
              <textarea
                value={text}
                onChange={(event) => setText(event.target.value)}
                className="min-h-[250px] flex-1 resize-none rounded-md border border-slate-300 bg-white p-3 text-base leading-7 text-slate-950 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                placeholder="Describe what the person shared, observed mood, or relevant context..."
              />
            </label>

            <label className="flex cursor-pointer flex-col gap-3 rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4 transition hover:border-blue-400 hover:bg-blue-50/40">
              <span className="flex items-center gap-2 text-sm font-medium text-slate-800">
                <FileAudio aria-hidden="true" size={18} />
                Audio upload
              </span>
              <input
                type="file"
                accept=".wav,.mp3,.m4a,.flac,.ogg,.webm,audio/*"
                className="sr-only"
                onChange={(event) => setAudio(event.target.files?.[0] || null)}
              />
              <span className="flex min-h-12 items-center gap-2 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700">
                <AudioLines aria-hidden="true" size={18} className="text-blue-600" />
                {audio ? audio.name : "Choose an audio file"}
              </span>
            </label>

            {error && (
              <div className="flex items-start gap-2 rounded-md border border-rose-200 bg-rose-50 p-3 text-sm text-rose-800">
                <AlertCircle aria-hidden="true" size={18} className="mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex min-h-11 flex-1 items-center justify-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
              >
                {isLoading ? <Loader2 aria-hidden="true" size={18} className="animate-spin" /> : <Sparkles aria-hidden="true" size={18} />}
                {isLoading ? "Analyzing" : "Generate Estimate"}
              </button>
              <button
                type="button"
                className="inline-flex min-h-11 items-center justify-center rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
                onClick={() => {
                  setText("");
                  setAudio(null);
                  setResult(null);
                  setError("");
                }}
              >
                Reset
              </button>
            </div>
          </form>

          <aside className="flex min-h-[620px] flex-col rounded-lg border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
            <div className="flex items-center gap-2 border-b border-slate-200 pb-4 text-blue-700">
              <ShieldCheck aria-hidden="true" size={20} />
              <h2 className="text-base font-semibold text-slate-950">Decision-Support Output</h2>
            </div>

            {result ? <ResultPanel result={result} audioName={audio?.name} /> : <EmptyState />}
          </aside>
        </section>

        <footer className="border-t border-slate-200 py-4 text-sm leading-6 text-slate-600">
          This prototype estimates risk signals from submitted inputs. It does not diagnose, replace clinical judgment, or provide emergency support.
        </footer>
      </div>
    </main>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-1 flex-col justify-center gap-4 py-10 text-slate-600">
      <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
        <Brain aria-hidden="true" size={28} />
      </div>
      <div>
        <p className="text-base font-medium text-slate-900">Awaiting input</p>
        <p className="mt-2 text-sm leading-6">
          Results will show a risk category, 0-100 score, confidence, probability split, and plain-language explanation.
        </p>
      </div>
    </div>
  );
}

function ResultPanel({ result, audioName }) {
  const categoryClass = categoryStyles[result.prediction] || "bg-slate-50 text-slate-800 border-slate-200";

  return (
    <div className="flex flex-1 flex-col gap-5 pt-5">
      <div className={`rounded-lg border p-4 ${categoryClass}`}>
        <p className="text-sm font-medium">Risk category</p>
        <p className="mt-1 text-2xl font-semibold tracking-normal">{result.prediction}</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Metric label="Score" value={`${result.score}/100`} />
        <Metric label="Confidence" value={`${Math.round(result.confidence * 100)}%`} />
      </div>

      <div>
        <div className="mb-2 flex items-center justify-between text-sm font-medium text-slate-800">
          <span>Probability split</span>
          <span className="text-slate-500">{result.model_version}</span>
        </div>
        <ProbabilityBar probabilities={result.probabilities} />
      </div>

      <ExplanationList title="Text explanation" items={result.text_explanation} />
      <ExplanationList title="Audio explanation" items={result.audio_explanation} />

      <div className="rounded-md bg-slate-100 p-3 text-sm leading-6 text-slate-700">
        Audio file: <span className="font-medium text-slate-900">{audioName || "No audio provided"}</span>
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
      <p className="text-xs font-medium uppercase text-slate-500">{label}</p>
      <p className="mt-1 text-xl font-semibold text-slate-950">{value}</p>
    </div>
  );
}

function ProbabilityBar({ probabilities }) {
  const low = Math.round(probabilities.low * 100);
  const moderate = Math.round(probabilities.moderate * 100);
  const high = Math.max(0, 100 - low - moderate);

  return (
    <div className="overflow-hidden rounded-md border border-slate-200 bg-slate-100">
      <div className="flex h-4 w-full">
        <div className="bg-emerald-500" style={{ width: `${low}%` }} />
        <div className="bg-amber-500" style={{ width: `${moderate}%` }} />
        <div className="bg-rose-500" style={{ width: `${high}%` }} />
      </div>
      <div className="grid grid-cols-3 gap-2 p-3 text-xs font-medium text-slate-700">
        <span>Low {low}%</span>
        <span>Moderate {moderate}%</span>
        <span>High {high}%</span>
      </div>
    </div>
  );
}

function ExplanationList({ title, items }) {
  return (
    <section>
      <h3 className="mb-2 text-sm font-semibold text-slate-950">{title}</h3>
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item} className="rounded-md border border-slate-200 bg-white p-3 text-sm leading-6 text-slate-700">
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default App;
