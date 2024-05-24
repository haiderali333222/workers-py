import uvicorn
from api.routes.index import api_router
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from utils.slack import slack_notify_error

app = FastAPI()
main_router = APIRouter()

main_router.include_router(api_router, prefix="")
app.include_router(main_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    slack_notify_error(error=exc, title="Internal Server Error", subtitle="An error occurred while processing the request")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)