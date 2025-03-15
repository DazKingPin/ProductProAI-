#!/bin/bash

# Deployment script for ProductPro AI
echo "Starting deployment of ProductPro AI..."

# Change to the project directory
cd "$(dirname "$0")"

# Install required dependencies
echo "Installing dependencies..."
pip install flask gunicorn

# Create deployment directory
DEPLOY_DIR="./build"
mkdir -p $DEPLOY_DIR

# Build frontend
echo "Building frontend..."
cd frontend
npm run build
cd ..

# Copy frontend build to deployment directory
echo "Copying frontend build..."
cp -r frontend/build/* $DEPLOY_DIR/

# Create startup script
echo "Creating startup script..."
cat > $DEPLOY_DIR/start.sh << 'EOF'
#!/bin/bash
# Start the ProductPro AI application
export FLASK_APP=backend/api/app.py
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:5000 backend.api.app:app
EOF

chmod +x $DEPLOY_DIR/start.sh

# Create systemd service file
echo "Creating systemd service file..."
cat > productpro.service << 'EOF'
[Unit]
Description=ProductPro AI Web Agent
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ProductProAI
ExecStart=/home/ubuntu/ProductProAI/build/start.sh
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=productpro

[Install]
WantedBy=multi-user.target
EOF

echo "Deployment preparation complete!"
echo "To start the application, run: ./build/start.sh"
echo "To install as a system service, copy productpro.service to /etc/systemd/system/ and run:"
echo "  sudo systemctl enable productpro.service"
echo "  sudo systemctl start productpro.service"
