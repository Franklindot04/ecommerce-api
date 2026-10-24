import json
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.cache_utils import invalidate_product_caches
from app.database import get_db
from app.models import Product
from app.redis_client import redis_client
from app.schemas import ProductCreate, ProductListResponse, ProductResponse

load_dotenv()

PRODUCT_CACHE_TTL = int(os.getenv("PRODUCT_CACHE_TTL", "60"))

router = APIRouter()


def serialize_product(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
    }


@router.get("/products", response_model=ProductListResponse)
async def get_products(
    page: int = Query(default=1, ge=1, description="Page number, starting at 1"),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of products per page, from 1 to 100",
    ),
    db: Session = Depends(get_db),
):
    cache_version = await redis_client.get("products:list:version") or "0"
    cache_key = f"products:list:v{cache_version}:page:{page}:size:{page_size}"
    cached_products = await redis_client.get(cache_key)

    if cached_products:
        return json.loads(cached_products)

    products_query = db.query(Product)
    total = products_query.count()
    products = (
        products_query.order_by(Product.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    result = {
        "items": [serialize_product(product) for product in products],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
    }

    await redis_client.setex(
        cache_key,
        PRODUCT_CACHE_TTL,
        json.dumps(result),
    )

    return result


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    cache_key = f"products:{product_id}"
    cached_product = await redis_client.get(cache_key)

    if cached_product:
        return json.loads(cached_product)

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    serialized = serialize_product(product)

    await redis_client.setex(
        cache_key,
        PRODUCT_CACHE_TTL,
        json.dumps(serialized),
    )

    return serialized


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    await invalidate_product_caches()

    return new_product
