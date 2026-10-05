#!/usr/bin/env bash
# ==============================================================================
# AWS EC2 One-Click Deployment Script for AI Investment Research Assistant
# Target OS: Ubuntu 22.04 LTS / 24.04 LTS on AWS EC2 (t3.medium / t3.small)
# ==============================================================================

set -e

echo "============================================================"
echo "  Deploying AI Investment Research Assistant to AWS EC2"
echo "============================================================"

# 1. Update system packages
echo "[1/6] Updating system packages..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common git

# 2. Configure 2GB Swap Memory (ensures stability on t3.small/t3.medium)
echo "[2/6] Configuring 2GB Swap Memory..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "    -> Swap configured successfully."
else
    echo "    -> Swap already present."
fi

# 3. Install Docker and Docker Compose
echo "[3/6] Installing Docker & Docker Compose..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "    -> Docker installed."
else
    echo "    -> Docker is already installed."
fi

# Install docker-compose plugin if needed
sudo apt-get install -y docker-compose-plugin

# 4. Prepare Application Directories
echo "[4/6] Creating persistent storage directories..."
mkdir -p data/chroma_db data/raw_pdfs data/processed

# 5. Environment configuration
echo "[5/6] Checking environment file (.env)..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "    -> Created .env from .env.example."
        echo "    -> [IMPORTANT] Edit .env with your GEMINI_API_KEY and AWS credentials:"
        echo "       nano .env"
    fi
else
    echo "    -> Existing .env found."
fi

# 6. Build and launch Docker container
echo "[6/6] Building and starting Docker container with Docker Compose..."
sudo docker compose down || true
sudo docker compose up -d --build

echo ""
echo "============================================================"
echo "  Deployment Complete! "
echo "============================================================"
echo "Application is running in detached mode."
echo "Access the Streamlit Dashboard at:"
echo "   http://$(curl -s http://checkip.amazonaws.com):8501"
echo ""
echo "Helpful commands:"
echo "   - View live logs:    sudo docker compose logs -f"
echo "   - Restart service:   sudo docker compose restart"
echo "   - Stop service:      sudo docker compose down"
echo "============================================================"
