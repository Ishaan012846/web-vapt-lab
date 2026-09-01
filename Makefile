.PHONY: help setup start check scan report stop reset test

PYTHON ?= python

help:
	@echo "Web Application VAPT Lab Commands:"
	@echo "  make setup    - Validate prerequisites and setup output folders"
	@echo "  make start    - Start OWASP Juice Shop docker container on 127.0.0.1:3000"
	@echo "  make check    - Run health check against Juice Shop container"
	@echo "  make scan     - Run scope validation, Nmap, and ZAP baseline scans"
	@echo "  make report   - Normalize scan findings and generate Markdown/HTML reports"
	@echo "  make test     - Run automated Python unit tests"
	@echo "  make stop     - Stop OWASP Juice Shop docker container"
	@echo "  make reset    - Reset lab environment (requires interactive confirmation)"

setup:
	$(PYTHON) scripts/setup_lab.py

start:
	docker-compose up -d
	@echo "Juice shop starting on http://127.0.0.1:3000..."

check:
	$(PYTHON) scripts/check_lab.py

scan:
	$(PYTHON) scripts/run_nmap.py
	$(PYTHON) scripts/run_zap.py

report:
	$(PYTHON) scripts/normalize_findings.py
	$(PYTHON) scripts/generate_report.py

test:
	$(PYTHON) -m pytest tests/ -v

stop:
	docker-compose down

reset:
	@echo "WARNING: This will stop containers and clear all generated output data."
	@read -p "Are you sure you want to reset the lab? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker-compose down -v --remove-orphans; \
		$(PYTHON) -c "import shutil, os; shutil.rmtree('output', ignore_errors=True); print('Output cleared.')"; \
		echo "Lab reset completed."; \
	else \
		echo "Reset cancelled."; \
	fi
