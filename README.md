# Intelligent BPM Lab

A process-independent, FHNW-ready LLM experiment wrapper with a Next.js interface and FastAPI backend.

## Features

- OpenAI, Claude, DeepSeek, Kimi, Qwen (editable model ID; Qwen region selector)
- Editable system instructions and case inputs
- Generic, invoice-exception and supplier-inquiry templates
- Import test cases from a JSON array (`[{"id":"EX-01","input":"...","expected":"..."}]`) or a plain-text file
- Run up to 20 selected cases per experiment
- Response times, provider usage tokens, raw model outputs, CSV exports, human-review template
- No payments or other write actions, no database, no persistence of API keys

## Local development

Requires Python 3.11+ and Node.js 20+.

Terminal 1:

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Terminal 2:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. Next.js proxies `/api/*` to the local FastAPI server.

## Vercel

The root `vercel.json` uses Vercel Services for `frontend/` and `backend/`. This feature may not be enabled for every account. Import this project at the repository root and deploy a *preview* first. If Services is unavailable, deploy the two folders as separate projects and configure the frontend proxy accordingly.

## Academic evaluation

1. Select a process module, then define the expected result for each case.
2. Run identical synthetic cases against different providers/models.
3. Export the experiment CSV and human-review template.
4. Manually assess correctness, unsupported assertions, next-action quality, response time and cost; record criteria and measurements in the paper.
5. Results are **not** automatically graded. Provider calls were not validated live without API keys.

## Security and limitations

- **Use synthetic data only.** Never submit real supplier records, personal data or confidential documents.
- API keys are held in browser state for the current page and forwarded via HTTPS to the backend and upstream provider. They are never intentionally logged or persisted in the application, but the provider processes requests under its own retention policies.
- Server requests go only to fixed provider endpoints. No custom provider URLs are permitted.
- No file storage. Import only text / JSON; no PDF/DOCX document parser is included.
- The demo does not execute approvals, send emails, or edit financial records.
- Restrict public access or add authentication and rate limiting before accepting real traffic. BYO-key public deployment has abuse and privacy risks.
