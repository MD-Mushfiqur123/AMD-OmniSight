"""
FastAPI Server & REST API for AMD-OmniSight
Provides real-time telemetry streaming and inference endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine import AMDOmniSightEngine
import uvicorn

app = FastAPI(title="AMD-OmniSight Edge Inference API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AMDOmniSightEngine()

@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "AMD-OmniSight Autonomous Vision Agent",
        "accelerator": "AMD ROCm 6.2 (Instinct MI300X / Radeon)",
        "architect": "Mushfiqur & L"
    }

@app.get("/api/v1/infer/{frame_id}")
def run_inference(frame_id: int):
    frame_data = engine.process_frame(frame_id)
    return frame_data.__dict__

@app.get("/api/v1/stats")
def get_stats():
    return {
        "total_frames_processed": engine.total_frames_processed,
        "total_anomalies_detected": engine.total_anomalies_detected,
        "backend": engine.backend
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
