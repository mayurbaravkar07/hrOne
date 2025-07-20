# routes/orders.py

from fastapi import APIRouter, HTTPException, Path, Query
from bson import ObjectId
from bson.errors import InvalidId
from models.order import Order
from database import order_collection, product_collection

router = APIRouter()

@router.post("/", status_code=201)
def create_order(order: Order):
    try:
        items = []

        for item in order.items:
            try:
                product_obj_id = ObjectId(item.productId)
            except InvalidId:
                raise HTTPException(status_code=400, detail=f"Invalid ObjectId format: {item.productId}")

            product = product_collection.find_one({"_id": product_obj_id})
            if not product:
                raise HTTPException(status_code=404, detail=f"Product not found in DB: {item.productId}")

            items.append({"productId": product_obj_id, "qty": item.qty})

        order_doc = {
            "userId": order.userId,
            "items": items
        }

        result = order_collection.insert_one(order_doc)
        return {"id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", status_code=200)
def get_orders(
    user_id: str = Path(...),
    limit: int = Query(default=10),
    offset: int = Query(default=0)
):
    try:
        query = {"userId": user_id}
        cursor = order_collection.find(query).sort("_id", 1).skip(offset).limit(limit)

        data = []

        for order in cursor:
            total = 0
            items = []

            for item in order.get("items", []):
                product = product_collection.find_one({"_id": item["productId"]})

                product_details = {
                    "name": product.get("name", "Unknown"),
                    "id": str(product.get("_id"))
                } if product else {}

                qty = item.get("qty", 0)
                price = product.get("price", 0) if product else 0
                total += qty * price

                items.append({
                    "productDetails": product_details,
                    "qty": qty
                })

            data.append({
                "id": str(order["_id"]),
                "items": items,
                "total": total
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

