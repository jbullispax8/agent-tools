#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up development environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}Installing required packages...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}Setup complete! Virtual environment is activated and packages are installed.${NC}"
echo -e "${BLUE}Available tools in this environment:${NC}"
echo "1. jira-cli: Command line interface for Jira operations"
echo "2. redshift-client: Interface for Redshift database operations"

echo -e "\n${BLUE}To activate the virtual environment in the future, run:${NC}"
echo "source venv/bin/activate" 