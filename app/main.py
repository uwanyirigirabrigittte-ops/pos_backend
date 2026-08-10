import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

from models import (
    category,
    supplier,
    product,
    user,
    customer,
    sale,
    sale_item,
    payment,
    receipt,
)

from routers import (
    category as category_router,
    supplier as supplier_router,
    product as product_router,
    user as user_router,
    customer as customer_router,
    sale as sale_router,
    sale_item as sale_item_router,
    payment as payment_router,
    receipt as receipt_router,
)

app = FastAPI(title="Bijoux's Store POS API", version="1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(sale_router)
app.include_router(sale_item_router)
app.include_router(payment_router)
app.include_router(receipt_router)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    for attempt in range(20):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully")
            break
        except Exception as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            time.sleep(3)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Bijoux'sStore Point of Sale Gateway Interface Engine"
    }
