import uvicorn
import os
from dotenv import load_dotenv

# set the environment variable
load_dotenv()
API_PORT = int(os.getenv("API_PORT"))

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=API_PORT,
    )
