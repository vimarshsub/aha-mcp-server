#!/bin/bash

# Aha! MCP Server Installation Script
# This script sets up the Aha! MCP Server on your system

set -e

echo "🚀 Aha! MCP Server Installation"
echo "================================"
echo

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"

# Check if pip is available
echo "📋 Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi
echo "✅ pip3 found"

# Create virtual environment (optional but recommended)
read -p "🤔 Create a virtual environment? (recommended) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv aha-mcp-env
    source aha-mcp-env/bin/activate
    echo "✅ Virtual environment created and activated"
    echo "💡 To activate later, run: source aha-mcp-env/bin/activate"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt
echo "✅ Dependencies installed"

# Configuration setup
echo "⚙️  Setting up configuration..."
if [ ! -f "aha_config.json" ]; then
    cp aha_config.json.example aha_config.json
    echo "📝 Created aha_config.json from example"
    echo "⚠️  Please edit aha_config.json with your Aha! credentials"
else
    echo "📝 aha_config.json already exists"
fi

# Test the installation
echo "🧪 Testing installation..."
if python3 -c "import aha_mcp_server; print('✅ Server module loads successfully')"; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    exit 1
fi

echo
echo "🎉 Installation completed successfully!"
echo
echo "📋 Next steps:"
echo "1. Edit aha_config.json with your Aha! credentials:"
echo "   - Set 'aha_domain' to your company's Aha! domain (e.g., 'yourcompany.aha.io')"
echo "   - Set 'api_key' to your Aha! API key"
echo
echo "2. Get your Aha! API key:"
echo "   - Log into Aha!"
echo "   - Go to Settings → Personal → Developer"
echo "   - Click 'Generate API key'"
echo
echo "3. Test the server:"
echo "   python3 aha_mcp_server.py"
echo
echo "4. Connect to Claude Desktop:"
echo "   Add the server configuration to your Claude Desktop MCP settings"
echo
echo "📚 Documentation:"
echo "   - README.md: Complete documentation"
echo "   - QUICKSTART.md: Quick setup guide"
echo "   - API_REFERENCE.md: Detailed API reference"
echo "   - examples.py: Usage examples"
echo
echo "🆘 Need help? Check the troubleshooting section in README.md"

