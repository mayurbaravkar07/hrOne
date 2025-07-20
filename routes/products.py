# routes/products.py

from fastapi import APIRouter, Query, HTTPException
from models.product import Product
from database import product_collection
from bson import ObjectId
import re

router = APIRouter()

@router.post("/", status_code=201)
def create_product(product: Product):
    try:
        product_dict = product.dict()
        result = product_collection.insert_one(product_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_products(
    name: str = Query(default=None),
    size: str = Query(default=None),
    limit: int = Query(default=10),
    offset: int = Query(default=0)
):
    query = {}

    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}  # partial search (case-insensitive)

    if size:
        query["sizes.size"] = size  # nested filter (e.g., sizes: [{size: "large"}])

    cursor = product_collection.find(query).sort("_id", 1).skip(offset).limit(limit)

    data = []
    for product in cursor:
        data.append({
            "id": str(product["_id"]),
            "name": product.get("name"),
            "price": product.get("price")
            # no sizes in output as per spec
        })

    response = {
        "data": data,
        "page": {
            "next": offset + limit,
            "limit": limit,
            "previous": offset - limit if offset - limit >= 0 else 0
        }
    }

    return response

