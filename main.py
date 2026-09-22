from fastapi import FastAPI

from routes.search import router as search_router

app = FastAPI(title="Google Organic Search Extractor", version="1.0.0")

app.include_router(search_router)
