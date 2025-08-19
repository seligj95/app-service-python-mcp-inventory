# Clothing Store Inventory MCP Server

A FastAPI-based clothing store inventory management application that exposes operations as MCP (Model Context Protocol) tools over HTTP and can be deployed to Azure App Service.

## Features

- ✅ **Inventory Management**: View, add, update, and delete clothing items
- 📏 **Size & Quantity Tracking**: Manage different sizes and stock quantities
- 🎯 **Category Organization**: Organize items by clothing categories
- 🌐 **Web Interface**: Clean, responsive UI with inventory display
- 🔧 **MCP Tools**: HTTP-accessible tools for external integrations
- 📋 **MCP URL Display**: Dynamic MCP server URL with one-click copy functionality
- ☁️ **Azure Ready**: Optimized for Azure App Service deployment

## MCP Tools Available

The application exposes the following MCP tools over HTTP:

- `get_inventory()` - Get all clothing items with sizes and quantities
- `add_item(name, category, price, sizes)` - Add a new clothing item
- `update_item_quantity(item_id, size, quantity)` - Update stock quantity for specific size
- `get_item_by_id(item_id)` - Get details of a specific item
- `search_items(query)` - Search items by name or category

## Local Development

### Prerequisites

- Python 3.11+
- Virtual environment (venv)

### Setup

1. Clone and setup environment:

```bash
cd app-service-python-mcp-inventory
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

4. Access the application:

   - Web Interface: http://localhost:8000/
   - Health Check: http://localhost:8000/health
   - MCP Endpoint: http://localhost:8000/mcp
   - MCP Tools: http://localhost:8000/mcp/tools/*

## Azure Deployment

### Prerequisites

- Azure CLI installed and logged in
- Azure Developer CLI (azd) installed

### Deploy with AZD

1. Initialize AZD:

```bash
azd init
```

2. Deploy to Azure:

```bash
azd up
```

### Infrastructure

The deployment creates:

- App Service Plan: P0V3 (Premium V3, Linux)
- App Service: Python 3.11 runtime with Uvicorn ASGI server

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │────│   FastAPI App    │────│   SQLite DB     │
│   (Inventory)   │    │   (Clothing API) │    │   (Inventory)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │   MCP Server     │
                       │   (HTTP Stream)  │
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │  External Tools  │
                       │  & Integrations  │
                       └──────────────────┘
```

## API Endpoints

### REST API

- `GET /api/inventory` - List all clothing items
- `POST /api/inventory` - Create new item
- `GET /api/inventory/{id}` - Get specific item
- `PUT /api/inventory/{id}` - Update item
- `DELETE /api/inventory/{id}` - Delete item

### MCP Integration

- `GET /mcp` - MCP server endpoint (HTTP streaming)
- `POST /mcp` - MCP protocol endpoint (JSON-RPC 2.0)
- `GET/POST /mcp/tools/get_inventory` - Direct tool access
- `POST /mcp/tools/add_item` - Direct tool access
- `POST /mcp/tools/update_item_quantity` - Direct tool access
- `GET/POST /mcp/tools/get_item_by_id` - Direct tool access
- `GET/POST /mcp/tools/search_items` - Direct tool access

## MCP Configuration

The application automatically displays the MCP server URL in the web interface with environment-aware detection:

- Local Development: `http://localhost:8000/mcp`
- Azure App Service: `https://your-app-name.azurewebsites.net/mcp`

### VS Code MCP Integration

To use this app as an MCP server in VS Code, add the following to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "clothing-inventory-mcp-server": {
      "url": "http://localhost:8000/mcp",
      "type": "http"
    }
  },
  "inputs": []
}
```

For the deployed Azure version, replace the URL with your App Service URL.

## Modifying Sample Data

Sample clothing items are defined in the `inventory_data.py` file. You can easily add, remove, or modify items by editing this file directly. The data includes:

- Item name, category, and price
- Available sizes (XS, S, M, L, XL, etc.)
- Stock quantities for each size

## License

This project is licensed under the MIT License.
