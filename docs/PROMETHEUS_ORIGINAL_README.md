# Prometheus

HR evidence workspace and fictional work-simulation lab, built for the Microsoft data-sovereignty hackathon challenge.

## Run

Install Python 3.11+ and uv. Copy `.env.example` to `.env` and add your API key, then:

```sh
cd prometheus
./run.sh
```

Open http://127.0.0.1:8765. Six fictional candidate fixtures are seeded automatically. To add the optional 30 public dataset CVs locally, run `uv run python import_public_cvs.py` and restart the server. Their authenticity is unverified; they remain unreviewed.

## Features and documentation

- [Application instructions](prometheus/README.md)
- [Architecture, evaluations and RL plan](hr_poc/README.md)
- [Simulation pitch deck](hr_poc/pitch/Prometheus_Simulation_Pitch.pptx)
- [Pitch script](hr_poc/pitch/SIMULATION_PITCH.md)

Run checks from `prometheus/` with `uv run python test_poc.py` and `uv run python test_simulation.py`.

This is a local demonstration with external inference, simulated roles and fictional simulation agents. It is not production authentication, private-cloud deployment or a validated employment assessment. Secrets, local databases and downloaded CV documents are excluded from version control.
