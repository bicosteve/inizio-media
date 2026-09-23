run:
	uvicorn main:app --reload

test:
	pytest -q

docker:
	docker compose up --build

no-cache:
	docker compose --progress=plain build --no-cache
