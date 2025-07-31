# AI Stock Selector - Dev Container Setup

This directory contains the development container configuration for the AI Stock Selector project.

## Files

- `devcontainer.json` - Main dev container configuration
- `setup.sh` - Post-creation setup script that installs TA-Lib and dependencies
- `install-talib.sh` - Standalone TA-Lib installation script
- `Dockerfile.backup` - Backup of original Dockerfile (not used)

## Quick Start

1. Open the project in VS Code
2. When prompted, select "Reopen in Container"
3. Wait for the container to build and setup to complete
4. TA-Lib and all dependencies will be automatically installed

## Container Features

- **Base Image**: Microsoft Python 3.11 dev container
- **TA-Lib**: Technical Analysis Library (automatically installed)
- **Python Packages**: All requirements from requirements.txt and requirements_enhanced.txt
- **Development Tools**: Black, Pylint, Jupyter, Git, GitHub CLI
- **VS Code Extensions**: Python, Jupyter, Copilot, and more

## Manual TA-Lib Installation

If needed, you can manually install TA-Lib using:

```bash
bash .devcontainer/install-talib.sh
```

## Verification

After container setup, verify TA-Lib installation:

```bash
verify-talib
```

## Ports

The following ports are forwarded for development:
- 8000, 8080: Web servers
- 5000: Flask development server  
- 3000: Node.js development server

## Troubleshooting

If you encounter issues:

1. Try rebuilding the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"
2. Check the setup log in the terminal
3. Manually run the TA-Lib installation script
