.PHONY: dev install clean seed test

dev:
	@echo "Starting backend on :8000 and frontend on :3000..."
	@cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000 &
	@cd frontend && npx vite --port 3000

install:
	cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

seed:
	cd backend && source .venv/bin/activate && python3 -c "from models.database import init_db; init_db()" && python3 ../ml/seed_roads.py && python3 -c "import sys; sys.path.insert(0,'../ml'); from seed_real_data import seed_all; seed_all()"

clean:
	rm -f backend/data/sih26002.db
	rm -rf backend/.venv
	rm -rf frontend/node_modules

test:
	cd backend && source .venv/bin/activate && python3 -c "from main import app; print('Backend OK')"
	cd frontend && npx tsc --noEmit && echo "Frontend OK"
