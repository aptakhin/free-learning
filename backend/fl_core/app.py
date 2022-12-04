"""."""
from typing import Union

from fastapi import FastAPI
from fl_core.routes import router


app = FastAPI()
app.include_router(router)
