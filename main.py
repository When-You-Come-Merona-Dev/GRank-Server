import uvicorn

from dotenv import load_dotenv
from core.config import config

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(
        app="app:app",
        host=config.WEB_SERVER_HOST,
        port=config.WEB_SERVER_PORT,
        reload=config.PROJ_RELOAD,
        workers=1,
    )
