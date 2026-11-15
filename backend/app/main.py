from fastapi import FastAPI

app = FastAPI(title="Stock Market Platform")


@app.get("/health")
def health():
    return {"status": "ok"}
