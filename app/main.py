import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import database
from app.api.endpoints import deserts, users, recepies, orders


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",)

app.include_router(users.auth_router, prefix="", tags=["Authentication"])
app.include_router(recepies.recipe_router, prefix="/recipes", tags=["Recipes management"])
app.include_router(deserts.desert_router, prefix="/deserts", tags=["Desert management"])
app.include_router(orders.order_router, prefix="/orders", tags=["Order management"])

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
