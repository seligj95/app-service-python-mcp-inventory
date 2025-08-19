# Python MCP Clothing Inventory Server Project

This is a Python-based MCP (Model Context Protocol) server for managing clothing store inventory that can be deployed to Azure App Service.

## Project Structure
- FastAPI-based MCP server
- SQLite database for inventory storage
- Azure App Service deployment with azd template
- Bicep infrastructure files

## Key Features
- Inventory management tools via MCP
- Web interface for inventory viewing
- Easy modification of sample data
- Azure deployment ready

## Development Instructions
- Use Python 3.11+
- FastAPI for web framework
- SQLite for data storage
- MCP protocol implementation

## Progress Tracking
- [x] Project requirements clarified
- [x] Project structure planned
- [x] Scaffold the project files
- [x] Customize for clothing inventory
- [x] Install required extensions
- [x] Compile and test
- [x] Create tasks
- [x] Launch project
- [x] Finalize documentation

## Local Development
Run `python main.py` or use the "Run MCP Inventory Server" task to start the development server.
Access the web interface at http://localhost:8000
MCP tools available at http://localhost:8000/mcp/tools/

## Azure Deployment
Use `azd init` and `azd up` to deploy to Azure App Service.
