UV=uv
BACKEND_DIR=backend

PORT=8000
HOST=0.0.0.0

message ?= "default commit message"
lib ?= "wirte library"

setup:
	cd $(BACKEND_DIR) && $(UV) sync

be-commit:
# message를 입력하시오
	cd $(BACKEND_DIR) && ruff format . && git add . && git commit -m "$(message)"

be-run:
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload --host=$(HOST) --port=$(PORT)

add:
# lib 값에 설치할 라이브러리를 입력하시오
	cd $(BACKEND_DIR) && uv pip install $(lib) && uv add $(lib)

