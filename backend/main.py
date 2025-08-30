from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Zoo Keeper AI Assistant API", description="AI assistant for zoo keepers that converts voice observations to structured data")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from routers import router
app.include_router(router)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Metrics endpoint
@app.get("/api/metrics")
async def get_metrics():
    """Get performance metrics"""
    # In a real implementation, we would collect and return actual metrics
    # For now, we'll return a placeholder response
    return {"metrics": "Performance metrics placeholder"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)