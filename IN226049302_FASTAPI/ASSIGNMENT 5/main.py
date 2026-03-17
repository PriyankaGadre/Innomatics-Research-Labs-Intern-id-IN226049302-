from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import math

app = FastAPI(title="Product and Order Management API", 
              description="API with search, sort, and pagination features",
              version="1.0.0")

# In-memory databases
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 3, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []
order_counter = 1

# Pydantic models
class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int
    total_price: float

class OrderResponse(BaseModel):
    order_id: int
    customer_name: str
    product_id: int
    quantity: int
    total_price: float

# ========== Q1: Search Endpoint (Already built) ==========
@app.get('/products/search')
def search_products(keyword: str = Query(..., description="Search keyword")):
    """
    Search products by name (case-insensitive)
    """
    results = [
        p for p in products
        if keyword.lower() in p['name'].lower()
    ]
    
    if not results:
        return {'message': f'No products found for: {keyword}'}
    
    return {
        'keyword': keyword,
        'total_found': len(results),
        'products': results
    }

# ========== Q2: Sort Endpoint (Already built) ==========
@app.get('/products/sort')
def sort_products(
    sort_by: str = Query('price', regex='^(price|name)$'),
    order: str = Query('asc', regex='^(asc|desc)$')
):
    """
    Sort products by price or name in ascending or descending order
    """
    reverse = (order == 'desc')
    sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=reverse)
    
    return {
        'sort_by': sort_by,
        'order': order,
        'total': len(sorted_products),
        'products': sorted_products
    }

# ========== Q3: Pagination Endpoint (Already built) ==========
@app.get('/products/page')
def get_products_paged(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(2, ge=1, le=20, description="Items per page")
):
    """
    Get paginated list of products
    """
    start = (page - 1) * limit
    end = start + limit
    total_pages = math.ceil(len(products) / limit)
    
    return {
        'page': page,
        'limit': limit,
        'total': len(products),
        'total_pages': total_pages,
        'products': products[start:end]
    }

# ========== Q4: Search Orders by Customer Name ==========
@app.post('/orders')
def create_order(order: Order):
    """
    Create a new order
    """
    global order_counter
    
    # Find product to get price
    product = next((p for p in products if p['id'] == order.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_order = {
        'order_id': order_counter,
        'customer_name': order.customer_name,
        'product_id': order.product_id,
        'product_name': product['name'],
        'quantity': order.quantity,
        'total_price': order.total_price,
        'status': 'pending'
    }
    orders.append(new_order)
    order_counter += 1
    
    return new_order

@app.get('/orders/search')
def search_orders(customer_name: str = Query(..., description="Customer name to search")):
    """
    Search orders by customer name (case-insensitive)
    """
    results = [
        o for o in orders
        if customer_name.lower() in o['customer_name'].lower()
    ]
    
    if not results:
        return {'message': f'No orders found for: {customer_name}'}
    
    return {
        'customer_name': customer_name,
        'total_found': len(results),
        'orders': results
    }

# ========== Q5: Sort Products by Category then Price ==========
@app.get('/products/sort-by-category')
def sort_by_category():
    """
    Sort products first by category alphabetically, then by price ascending
    """
    # Sort by category first, then by price
    result = sorted(products, key=lambda p: (p['category'], p['price']))
    
    return {
        'products': result,
        'total': len(result),
        'sorted_by': 'category → price'
    }

# ========== Q6: Search + Sort + Paginate in One Endpoint ==========
@app.get('/products/browse')
def browse_products(
    keyword: Optional[str] = Query(None, description="Search keyword"),
    sort_by: str = Query('price', regex='^(price|name)$', description="Sort field"),
    order: str = Query('asc', regex='^(asc|desc)$', description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(4, ge=1, le=20, description="Items per page")
):
    """
    Browse products with search, sort, and pagination all in one
    """
    # Step 1: Search (filter by keyword if provided)
    result = products
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p['name'].lower()
        ]
    
    # Step 2: Sort
    if sort_by in ['price', 'name']:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == 'desc'))
    
    # Step 3: Paginate
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]
    total_pages = math.ceil(total / limit) if total > 0 else 0
    
    return {
        'keyword': keyword,
        'sort_by': sort_by,
        'order': order,
        'page': page,
        'limit': limit,
        'total_found': total,
        'total_pages': total_pages,
        'products': paged
    }

# ========== BONUS: Paginate Orders ==========
@app.get('/orders/page')
def get_orders_paged(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(3, ge=1, le=20, description="Items per page")
):
    """
    Get paginated list of orders
    """
    start = (page - 1) * limit
    end = start + limit
    total_orders = len(orders)
    total_pages = math.ceil(total_orders / limit) if total_orders > 0 else 0
    
    return {
        'page': page,
        'limit': limit,
        'total': total_orders,
        'total_pages': total_pages,
        'orders': orders[start:end]
    }

# ========== Additional helper endpoint ==========
@app.get('/products/{product_id}')
def get_product(product_id: int):
    """
    Get a specific product by ID
    """
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get('/')
def root():
    return {
        'message': 'FastAPI Day 6 Assignment',
        'endpoints': [
            '/products/search?keyword=mouse',
            '/products/sort?sort_by=price&order=asc',
            '/products/page?page=1&limit=2',
            '/orders/search?customer_name=rahul',
            '/products/sort-by-category',
            '/products/browse?keyword=e&sort_by=price&page=1&limit=2',
            '/orders/page?page=1&limit=3'
        ]
    }