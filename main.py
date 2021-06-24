import uvicorn

from dotenv import load_dotenv
from src.config import config
from src import create_app

app = create_app()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(
        app="main:app",
        host=config.WEB_SERVER_HOST,
        port=config.WEB_SERVER_PORT,
        reload=config.PROJ_RELOAD,
        workers=1,
    )
