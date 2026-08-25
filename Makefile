# ==============================================================================
# PAIMANA AI - Makefile
# ==============================================================================

.PHONY: help install seed train score test run build docker bundle clean

help:
	@echo "PAIMANA AI - Command Menu:"
	@echo "  make install   - Install Python and Node dependencies"
	@echo "  make seed      - Generate 1,000 project CUF dataset"
	@echo "  make train     - Train XGBoost models & temporal evaluation"
	@echo "  make score     - Run hybrid risk scoring & alerts engine"
	@echo "  make test      - Run all 26 automated tests & system audit"
	@echo "  make run       - Launch full application (backend + frontend + health check)"
	@echo "  make build     - Build production React frontend bundle"
	@echo "  make docker    - Build and launch via docker-compose"
	@echo "  make bundle    - Refresh complete codebase single-text bundle"
	@echo "  make clean     - Remove cache, temp build artifacts, and test logs"

install:
	pip install -r requirements.txt
	cd frontend && npm install

seed:
	python src/data_gen/generate_data.py --n-projects 1000

train:
	python src/models/train_and_evaluate.py

score:
	python src/risk_engine/scorer.py

test:
	pytest tests/ -v
	python scripts/system_health_check.py

run:
	python scripts/run_system.py

build:
	cd frontend && npm run build

bundle:
	python scripts/export_codebase.py

docker:
	docker-compose up --build

clean:
	python -c "import shutil, pathlib, os; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache','frontend/dist','frontend/node_modules/.vite','__pycache__']]; [shutil.rmtree(str(p), ignore_errors=True) for p in pathlib.Path('src').rglob('__pycache__')]; print('clean done')"
