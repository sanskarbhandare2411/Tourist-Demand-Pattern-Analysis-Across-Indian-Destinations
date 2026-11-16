"""
FastAPI Serverless Application Entry Point
Tourist Demand Pattern Analysis Across Indian Destinations
"""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Ensure repository root is on sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from api.routes import (
    overview,
    destinations,
    demand,
    seasonal,
    weather,
    ml,
    clustering,
    recommendations,
    meta
)

app = FastAPI(
    title="Tourist Demand Pattern Analysis API",
    description="Backend intelligence API for Indian Tourism Demand Analysis, ML Forecasting, Clustering, and Recommendations.",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Enable CORS for frontend and deployment domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(overview.router)
app.include_router(destinations.router)
app.include_router(demand.router)
app.include_router(seasonal.router)
app.include_router(weather.router)
app.include_router(ml.router)
app.include_router(clustering.router)
app.include_router(recommendations.router)
app.include_router(meta.router)


@app.get("/api")
def api_root():
    return {
        "platform": "Tourist Demand Pattern Analysis Across Indian Destinations",
        "status": "online",
        "version": "2.0.0",
        "docs": "/api/docs",
        "endpoints": [
            "/api/overview",
            "/api/destinations",
            "/api/destinations/map",
            "/api/destinations/rankings",
            "/api/destinations/typology-impact",
            "/api/demand/longitudinal",
            "/api/demand/statewise",
            "/api/demand/composition",
            "/api/seasonal/quarterly",
            "/api/seasonal/breakdown",
            "/api/seasonal/summary",
            "/api/weather/temperature",
            "/api/weather/rainfall",
            "/api/weather/correlation",
            "/api/ml/metrics",
            "/api/ml/predict",
            "/api/clustering/overview",
            "/api/clustering/evaluation",
            "/api/clustering/profiles",
            "/api/clustering/members",
            "/api/recommendations/strategies",
            "/api/recommendations/decongestion",
            "/api/recommendations/weather",
            "/api/recommendations/seasonal",
            "/api/recommendations/filter",
            "/api/meta/health",
            "/api/meta/filters"
        ]
    }


# Static React SPA Mount (for local & preview server deployment)
DIST_DIR = ROOT_DIR / "frontend" / "dist"
if (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")


@app.get("/{full_path:path}")
def serve_frontend_spa(full_path: str = ""):
    if full_path.startswith("api"):
        return JSONResponse(status_code=404, content={"detail": f"API endpoint /{full_path} not found"})
    target = DIST_DIR / full_path
    if target.is_file():
        return FileResponse(target)
    index_file = DIST_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "platform": "Tourist Demand Pattern Analysis Across Indian Destinations",
        "status": "online",
        "version": "2.0.0",
        "docs": "/api/docs"
    }
