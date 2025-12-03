#!/bin/bash
# Installation script for GitHub API integration

echo "================================================"
echo "GitHub API Integration Installer"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a Frappe bench directory
if [ ! -d "env" ]; then
    echo -e "${RED}❌ Error: Not in a Frappe bench directory${NC}"
    echo "Please run this script from your frappe-bench directory"
    exit 1
fi

echo -e "${YELLOW}Step 1: Installing Python dependencies...${NC}"
source env/bin/activate
pip install requests
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Clearing Frappe cache...${NC}"
bench clear-cache
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Cache cleared${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: Cache clear failed (not critical)${NC}"
fi

echo ""
echo -e "${YELLOW}Step 3: Building assets...${NC}"
bench build
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Assets built${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: Build failed (not critical)${NC}"
fi

echo ""
echo -e "${YELLOW}Step 4: Restarting Frappe...${NC}"
bench restart
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frappe restarted${NC}"
else
    echo -e "${RED}❌ Failed to restart Frappe${NC}"
    exit 1
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Open your Frappe site in a browser"
echo "2. Click the chatbot icon (🤖) in the navbar"
echo "3. Try these commands:"
echo "   - 'Show repo info'"
echo "   - 'Show recent commits'"
echo "   - 'Show open issues'"
echo ""
echo "Optional: Add GitHub token for higher rate limits"
echo "See README_GITHUB_SETUP.md for instructions"
echo ""
echo "Test the integration:"
echo "  cd apps/itchamps"
echo "  python test_github_integration.py"
echo ""
