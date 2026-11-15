# CommonGround

Company and people digital twins prepare better conversations at recruitment events.

Built for the City of Espoo Junction challenge. A participant chooses a company, reviews the evidence represented by each twin and explores an explicit work-scenario assumption. The result shows shared evidence, uncertainty and a meeting agenda. Both sides must opt in before the demo records meeting feedback.

## Run locally

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```sh
./run.sh
```

Open http://127.0.0.1:8766 . The default binds only to your computer. No model is required for the local scenarios.

```sh
uv run --project prometheus python -m unittest discover -s tests -v
```

## Demo route

1. Choose Harbor Services and Robin Lee, the same fictional pair shown in the video.
2. Run the incident scenario and inspect the missing data-validation example.
3. Prepare an introduction and simulate each party's opt-in to reveal the shared agenda.
4. Edit and approve a twin. Earlier runs remain inspectable but cannot create current introductions.
5. Explore Northstar Commerce for the fixed SQL benchmark and explicit repair assumptions.
6. Export a JSON evidence receipt or print a confirmed meeting agenda.


## Live model

Optional live dialogue uses an OpenAI-compatible gateway. Set `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` in an ignored `.env.local`, or environment variables. Local configuration overrides the original `.env`; environment variables override both. The demo allowlist supports the original DataCrunch endpoint and the configured TalentAdore LiteLLM gateway. Provider changes require an explicit allowlist edit.

Gemini 2.5 Flash through the existing Aaltoes hackathon gateway was tested for this project. Credentials are local only. The original Microsoft endpoint returned HTTP 404. The request sends fictional descriptions and evidence; dedicated name/location fields are omitted, but editable free text is **not anonymized**. Provider retention/residency has not been verified. Model failure stays visible and never turns fixture dialogue into a claimed live response.

## What the result means

A twin is an editable representation of supplied evidence and assumptions. It is not a psychological model of a person. Evidence coverage counts company-requested skill areas with a supplied reference. The revenue benchmark checks an explicitly selected SQL strategy against fixed synthetic data. Changing company prose does not change that benchmark. Neither result is a probability of hiring success.

The current implementation is a single-user synthetic demo. Identity, ownership and independent consent are simulated. No external invitations are sent. Do not expose this server publicly or enter real CVs without implementing authentication, tenant isolation, retention/deletion and provider controls. CV file extraction and job-application submission are outside this prototype; work examples are entered as text.

## Structure

- `commonground_app/`: new Espoo API, frontend and fictional fixtures.
- `tests/`: lifecycle, consent, scenario and failure tests.
- `submission/`: pitch deck, PDF, narrated demo, submission text and handoff.
- `prometheus/`: reused fixed SQL checks and dependency manifest.
- `docs/PROMETHEUS_ORIGINAL_README.md`: original README preserved.

## Provenance

This repository is a clean publication snapshot of the CommonGround adaptation. Original Prometheus material and history remain in the owner’s private working copy; only the reused benchmark and dependency files are included here. The new CommonGround interface, event flow, twin API, versioning, introductions, tests and Espoo pitch were created in this adaptation. `prometheus/simulation.py` is reused, with a connection cleanup fix. This project does not claim that all code originated at Junction.

On 15 November 2026, the project owner explicitly confirmed organiser approval for this reuse. No written approval document is stored in the repository. Official rules and challenge links are in `submission/SOURCES.md`.

## Judge package

[Public demo, revised video and pitch](https://commonground-espoo-junction-2026.oaken-trail-6302.chatgpt.site). The browser preview makes no model calls and uses fictional session data.
