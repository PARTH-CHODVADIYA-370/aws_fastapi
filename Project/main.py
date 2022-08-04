import uvicorn

if __name__ == "__main__":
    uvicorn.run("Server.app:app", host="localhost", lifespan="on", reload=True)
