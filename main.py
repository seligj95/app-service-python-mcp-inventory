"""
Clothing Store Inventory MCP Server
A FastAPI application that provides MCP tools for inventory management
"""

import json
import os
import sqlite3
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from inventory_data import SAMPLE_INVENTORY


# Pydantic models
class InventoryItem(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str
    sizes: Dict[str, int]


class CreateItemRequest(BaseModel):
    name: str
    category: str
    price: float
    description: str
    sizes: Dict[str, int]


class UpdateQuantityRequest(BaseModel):
    item_id: int
    size: str
    quantity: int


# Database setup
def init_database():
    """Initialize SQLite database with sample data"""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item_sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            size TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
    ''')
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM items')
    if cursor.fetchone()[0] == 0:
        # Insert sample data
        for item in SAMPLE_INVENTORY:
            cursor.execute('''
                INSERT INTO items (id, name, category, price, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (item['id'], item['name'], item['category'], item['price'], item['description']))
            
            for size, quantity in item['sizes'].items():
                cursor.execute('''
                    INSERT INTO item_sizes (item_id, size, quantity)
                    VALUES (?, ?, ?)
                ''', (item['id'], size, quantity))
    
    conn.commit()
    conn.close()


def get_inventory() -> List[Dict[str, Any]]:
    """Get all inventory items with sizes and quantities"""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT i.id, i.name, i.category, i.price, i.description
        FROM items i
        ORDER BY i.category, i.name
    ''')
    items = cursor.fetchall()
    
    result = []
    for item in items:
        item_id, name, category, price, description = item
        
        # Get sizes and quantities
        cursor.execute('''
            SELECT size, quantity
            FROM item_sizes
            WHERE item_id = ?
        ''', (item_id,))
        sizes_data = cursor.fetchall()
        sizes = {size: quantity for size, quantity in sizes_data}
        
        result.append({
            'id': item_id,
            'name': name,
            'category': category,
            'price': price,
            'description': description,
            'sizes': sizes
        })
    
    conn.close()
    return result


def get_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific item by ID"""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT i.id, i.name, i.category, i.price, i.description
        FROM items i
        WHERE i.id = ?
    ''', (item_id,))
    item = cursor.fetchone()
    
    if not item:
        conn.close()
        return None
    
    item_id, name, category, price, description = item
    
    # Get sizes and quantities
    cursor.execute('''
        SELECT size, quantity
        FROM item_sizes
        WHERE item_id = ?
    ''', (item_id,))
    sizes_data = cursor.fetchall()
    sizes = {size: quantity for size, quantity in sizes_data}
    
    conn.close()
    return {
        'id': item_id,
        'name': name,
        'category': category,
        'price': price,
        'description': description,
        'sizes': sizes
    }


def add_item(name: str, category: str, price: float, description: str, sizes: Dict[str, int]) -> Dict[str, Any]:
    """Add a new item to inventory"""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO items (name, category, price, description)
        VALUES (?, ?, ?, ?)
    ''', (name, category, price, description))
    
    item_id = cursor.lastrowid
    
    for size, quantity in sizes.items():
        cursor.execute('''
            INSERT INTO item_sizes (item_id, size, quantity)
            VALUES (?, ?, ?)
        ''', (item_id, size, quantity))
    
    conn.commit()
    conn.close()
    
    return get_item_by_id(item_id)


def update_item_quantity(item_id: int, size: str, quantity: int) -> bool:
    """Update quantity for a specific item size"""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE item_sizes
        SET quantity = ?
        WHERE item_id = ? AND size = ?
    ''', (quantity, item_id, size))
    
    affected_rows = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected_rows > 0


def search_items(query: str) -> List[Dict[str, Any]]:
    """Search items by name or category"""
    all_items = get_inventory()
    query = query.lower()
    
    return [
        item for item in all_items
        if query in item['name'].lower() or query in item['category'].lower()
    ]


# FastAPI application setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database()
    yield
    # Shutdown (nothing to do)


app = FastAPI(
    title="Clothing Store Inventory MCP Server",
    description="MCP server for managing clothing store inventory",
    version="1.0.0",
    lifespan=lifespan
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# MCP Tool Functions
async def mcp_get_inventory() -> Dict[str, Any]:
    """MCP tool: Get all inventory items"""
    items = get_inventory()
    return {
        "items": items,
        "total_items": len(items),
        "categories": list(set(item['category'] for item in items))
    }


async def mcp_add_item(name: str, category: str, price: float, description: str = "", sizes: Dict[str, int] = None) -> Dict[str, Any]:
    """MCP tool: Add a new clothing item"""
    if sizes is None:
        sizes = {"S": 0, "M": 0, "L": 0}
    
    item = add_item(name, category, price, description, sizes)
    return {"success": True, "item": item}


async def mcp_update_item_quantity(item_id: int, size: str, quantity: int) -> Dict[str, Any]:
    """MCP tool: Update quantity for a specific item and size"""
    success = update_item_quantity(item_id, size, quantity)
    if success:
        item = get_item_by_id(item_id)
        return {"success": True, "item": item}
    else:
        return {"success": False, "error": "Item or size not found"}


async def mcp_get_item_by_id(item_id: int) -> Dict[str, Any]:
    """MCP tool: Get a specific item by ID"""
    item = get_item_by_id(item_id)
    if item:
        return {"success": True, "item": item}
    else:
        return {"success": False, "error": "Item not found"}


async def mcp_search_items(query: str) -> Dict[str, Any]:
    """MCP tool: Search items by name or category"""
    items = search_items(query)
    return {
        "items": items,
        "count": len(items),
        "query": query
    }


# MCP Tools Registry
MCP_TOOLS = {
    "get_inventory": {
        "function": mcp_get_inventory,
        "description": "Get all clothing items in inventory with sizes and quantities",
        "parameters": {}
    },
    "add_item": {
        "function": mcp_add_item,
        "description": "Add a new clothing item to inventory",
        "parameters": {
            "name": {"type": "string", "description": "Name of the clothing item"},
            "category": {"type": "string", "description": "Category (e.g., T-Shirts, Jeans, Dresses)"},
            "price": {"type": "number", "description": "Price of the item"},
            "description": {"type": "string", "description": "Item description", "optional": True},
            "sizes": {"type": "object", "description": "Sizes and quantities (e.g., {\"S\": 10, \"M\": 15})", "optional": True}
        }
    },
    "update_item_quantity": {
        "function": mcp_update_item_quantity,
        "description": "Update stock quantity for a specific item and size",
        "parameters": {
            "item_id": {"type": "integer", "description": "ID of the item"},
            "size": {"type": "string", "description": "Size to update"},
            "quantity": {"type": "integer", "description": "New quantity"}
        }
    },
    "get_item_by_id": {
        "function": mcp_get_item_by_id,
        "description": "Get details of a specific item by ID",
        "parameters": {
            "item_id": {"type": "integer", "description": "ID of the item"}
        }
    },
    "search_items": {
        "function": mcp_search_items,
        "description": "Search items by name or category",
        "parameters": {
            "query": {"type": "string", "description": "Search query"}
        }
    }
}


# Web Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page showing inventory"""
    items = get_inventory()
    
    # Calculate statistics
    categories = list(set(item['category'] for item in items))
    total_stock = sum(sum(item['sizes'].values()) for item in items)
    
    # Get the current host for MCP URL
    host = request.headers.get("host", "localhost:8000")
    protocol = "https" if request.headers.get("x-forwarded-proto") == "https" else "http"
    mcp_url = f"{protocol}://{host}/mcp"
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "items": items,
        "mcp_url": mcp_url,
        "categories": categories,
        "total_stock": total_stock
    })


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "clothing-inventory-mcp"}


# API Routes
@app.get("/api/inventory")
async def api_get_inventory():
    """REST API: Get all inventory items"""
    return get_inventory()


@app.get("/api/inventory/{item_id}")
async def api_get_item(item_id: int):
    """REST API: Get specific item"""
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/api/inventory")
async def api_create_item(item: CreateItemRequest):
    """REST API: Create new item"""
    return add_item(item.name, item.category, item.price, item.description, item.sizes)


@app.patch("/api/inventory/{item_id}/quantity")
async def api_update_quantity(item_id: int, update: UpdateQuantityRequest):
    """REST API: Update item quantity"""
    success = update_item_quantity(update.item_id, update.size, update.quantity)
    if not success:
        raise HTTPException(status_code=404, detail="Item or size not found")
    return get_item_by_id(item_id)


# MCP Routes
@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP server endpoint for JSON-RPC 2.0 over HTTP"""
    if request.method == "GET":
        return {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "clothing-inventory-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    # Handle POST requests (JSON-RPC 2.0)
    body = await request.json()
    method = body.get("method", "")
    
    # Handle initialization
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": "clothing-inventory-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    # Handle tool listing
    elif method == "tools/list":
        tools = []
        for tool_name, tool_info in MCP_TOOLS.items():
            tools.append({
                "name": tool_name,
                "description": tool_info["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": tool_info["parameters"]
                }
            })
        
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {"tools": tools}
        }
    
    # Handle tool calls
    elif method == "tools/call":
        tool_name = body.get("params", {}).get("name")
        arguments = body.get("params", {}).get("arguments", {})
        
        if tool_name in MCP_TOOLS:
            try:
                result = await MCP_TOOLS[tool_name]["function"](**arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Tool '{tool_name}' not found"
                }
            }
    
    # Handle notifications
    elif method == "notifications/initialized":
        # Just acknowledge the notification
        return None
    
    # Unknown method
    else:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found"
            }
        }


# Direct MCP tool access
@app.get("/mcp/tools/{tool_name}")
@app.post("/mcp/tools/{tool_name}")
async def mcp_tool_direct(tool_name: str, request: Request):
    """Direct access to MCP tools"""
    if tool_name not in MCP_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    if request.method == "GET":
        # For GET requests, return tool info
        return {
            "tool": tool_name,
            "description": MCP_TOOLS[tool_name]["description"],
            "parameters": MCP_TOOLS[tool_name]["parameters"]
        }
    
    # For POST requests, execute the tool
    try:
        if request.headers.get("content-type") == "application/json":
            arguments = await request.json()
        else:
            arguments = {}
        
        result = await MCP_TOOLS[tool_name]["function"](**arguments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
