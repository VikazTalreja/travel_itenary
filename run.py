import uvicorn
import os
from app.database import models
from app.database.database import engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 