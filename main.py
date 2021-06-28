import uvicorn

from dotenv import load_dotenv
from src.config import CONFIG
from src import create_app

app = create_app()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(
        app="main:app",
        host=CONFIG.WEB_SERVER_HOST,
        port=CONFIG.WEB_SERVER_PORT,
        reload=CONFIG.PROJ_RELOAD,
        workers=1,
    )
