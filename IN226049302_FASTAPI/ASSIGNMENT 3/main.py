from fastapi import FastAPI, Response, status, Query

app = FastAPI()

# Initial products list
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# helper function
def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

@app.get("/products/audit")
def product_audit():
    in_stock_products = [p for p in products if p["in_stock"]]
    out_stock_products = [p for p in products if not p["in_stock"]]
    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)
    most_expensive = max(products, key=lambda p: p["price"])
    
    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": [p["name"] for p in out_stock_products],
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}
    return product

@app.post("/products")
def add_product(product: dict, response: Response):
    for p in products:
        if p["name"] == product["name"]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product already exists"}

    next_id = max(p["id"] for p in products) + 1
    new_product = {
        "id": next_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "in_stock": product.get("in_stock", True)
    }

    products.append(new_product)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Product added", "product": new_product}

@app.put("/products/{product_id}")
def update_product(product_id: int, response: Response,
                   price: int | None = None,
                   in_stock: bool | None = None):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price
    if in_stock is not None:
        product["in_stock"] = in_stock

    return {"message": "Product updated", "product": product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)
    return {"message": f"Product '{product['name']}' deleted"}