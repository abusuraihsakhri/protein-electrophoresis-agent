# Protein Electrophoresis Agent

A Python repository containing experimental, rule-based demonstrations for synthetic laboratory measurements, with command-line tools, FastAPI endpoints, tests, and a standalone browser interface.

**Clinical limitation:** The current implementations do **not** quantify an M-spike from an electrophoretic trace or establish SPEP/UPEP diagnoses. Their unitless thresholds (including 20, 25, 10, and 12 in different legacy modules) are illustrative, not validated clinical cutoffs. No diagnostic, therapeutic, or emergency decision should be based on these outputs.

## Browser demonstration

Open `web/index.html` in a current desktop or mobile browser. Enter **synthetic** task and specimen IDs plus generic primary and secondary values, then select **Evaluate demo rules**. View the actual locally computed flags and export the JSON result. There is no simulated API response, HMAC signing, or backend dependency.

The browser demonstration is implemented in plain JavaScript; Python-in-the-browser is unnecessary for these simple example rules. It makes no network requests for evaluation and does not persist case data across page reloads. Do not enter clinical or personally identifying information.

## Python installation

Requires Python 3.9 or newer. From the repository root:

```bash
python -m pip install -e '.[api,test]'
python -m pytest -q
```

For core CLI use without HTTP support, `python -m pip install -e .` is sufficient.

## Commands

The installed `protein-electrophoresis-engine` command uses the `protein_electrophoresis_agent` demonstration package:

```bash
protein-electrophoresis-engine audit --case-id DEMO-001 --primary 10 --secondary 2 --status NORMAL
protein-electrophoresis-engine batch -i sample.csv -o results.csv
protein-electrophoresis-engine chat status
protein-electrophoresis-engine serve --host 127.0.0.1 --port 8000
```

The repository also includes a **separate legacy CLI** with a different payload schema and rule thresholds:

```bash
python cli.py audit --task-id DEMO-001 --target SYNTH-001 --primary 10 --secondary 2
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000
```

The legacy Python API provides `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs`. The packaged clinical demonstration API has a different request format, so its endpoints are not interchangeable. The server listens only on loopback by default.

CSV flags `True`/`False`, `1`/`0`, and `yes`/`no` are recognized case-insensitively. Invalid boolean rows are skipped with a warning.

## Privacy and security limitations

The browser page processes demonstration inputs locally. The Python services handle submitted data **on the host running the server**, and their in-memory registries and audit trails are not designed for regulated clinical workloads. A small set of regular-expression identifier checks is provided, but it is not comprehensive de-identification or HIPAA Safe Harbor verification. The audit trail uses in-memory HMAC chaining and is not durable across process restarts.

For persistent Python audit-chain signing, set a unique `AUDIT_SECRET_KEY` in the server's environment. Docker Compose requires this variable instead of providing a shared secret. Keep the server private unless appropriate authentication, authorization, transport protection, monitoring, and data governance are added.

## Development and verification

```bash
python -m compileall -q agents protein_electrophoresis_agent
python -m pytest -q
node --check web/app.js
node tests/browser_logic.cjs
```

CI runs Python checks on Python 3.10–3.12 and Node-based browser-logic tests. The standalone browser does not require Node.js to use; Node is only for test execution.

Technology: Python, Pydantic, optional FastAPI/Uvicorn, standard JavaScript, HTML, and CSS. The browser demonstration is compatible with modern browsers supporting ES2018 JavaScript and `Blob` downloads.

## Scope and known gaps

The repository retains several historical CLI and API variants with inconsistent example thresholds and terminology. Neither the browser demo nor the Python examples performs validated densitometric peak integration, immunofixation interpretation, or free light-chain testing. Rigorous clinical rules, validated reference data, and specimen-level verification would be required before offering a real protein electrophoresis interpretation tool.

## License

MIT. See [LICENSE](LICENSE).
