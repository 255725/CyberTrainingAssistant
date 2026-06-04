from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import biceps
import barki
import wyskok


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/video-stream/{exercise_id}")
def start_exercise(exercise_id: str):
    if exercise_id == "1":
        return StreamingResponse(biceps.generuj_obraz_biceps(), media_type="multipart/x-mixed-replace; boundary=frame")
    elif exercise_id == "2":
        return StreamingResponse(barki.generuj_obraz_barki(), media_type="multipart/x-mixed-replace; boundary=frame")
    elif exercise_id == "3":
        return StreamingResponse(wyskok.generuj_obraz_wyskok(), media_type="multipart/x-mixed-replace; boundary=frame")
    
@app.post("/api/stop-exercise")
def stop_exercise():
    biceps.zatrzymaj_trening()
    barki.zatrzymaj_trening()
    wyskok.zatrzymaj_trening()
    return {"status": "success", "message": "Kamery wyłączone awaryjnie"}