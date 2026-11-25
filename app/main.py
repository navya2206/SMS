from fastapi import FastAPI
app = FastAPI(title="Student Management System")
@app.get("/health")
def health():
    return {"status": "ok"}