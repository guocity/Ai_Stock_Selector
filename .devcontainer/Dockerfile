# Use official Python base image with Ubuntu
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    tar \
    curl \
    git \
    vim \
    nano \
    htop \
    tree \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib C library
RUN cd /tmp && \
    wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr/local && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    # Create symbolic links
    ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so && \
    ln -sf /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta_lib.so.0 && \
    # Cleanup
    cd / && rm -rf /tmp/ta-lib*

# Set TA-Lib environment variables
ENV TA_INCLUDE_PATH=/usr/local/include
ENV TA_LIBRARY_PATH=/usr/local/lib
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Upgrade pip and install Python packages
RUN python -m pip install --upgrade pip setuptools wheel

# Install TA-Lib Python wrapper
RUN pip install TA-Lib

# Install common data science and financial analysis packages
RUN pip install \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scipy \
    scikit-learn \
    jupyter \
    jupyterlab \
    plotly \
    yfinance \
    akshare \
    requests \
    beautifulsoup4 \
    lxml \
    openpyxl \
    xlsxwriter \
    python-dotenv \
    pydantic \
    fastapi \
    uvicorn \
    streamlit \
    dash \
    flask \
    sqlalchemy \
    psycopg2-binary \
    pymongo \
    redis \
    celery

# Install development tools
RUN pip install \
    black \
    isort \
    flake8 \
    pylint \
    mypy \
    pytest \
    pytest-cov \
    pre-commit \
    autopep8 \
    bandit

# Create workspace directory
WORKDIR /workspace

# Create cache directory for the user
RUN mkdir -p /home/vscode/.cache && \
    chown -R vscode:vscode /home/vscode/.cache

# Create verification script
RUN cat > /usr/local/bin/verify-talib << 'EOF'
#!/usr/bin/env python3
"""Verify TA-Lib installation in container"""
try:
    import talib
    import numpy as np
    
    # Test data
    test_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    
    # Test indicators
    sma = talib.SMA(test_data, timeperiod=5)
    rsi = talib.RSI(test_data, timeperiod=14)
    macd, signal, hist = talib.MACD(test_data)
    
    print("✅ TA-Lib is working correctly in the container!")
    print(f"✅ Version: {talib.__version__}")
    print("✅ All basic indicators tested successfully")
    
except Exception as e:
    print(f"❌ TA-Lib verification failed: {e}")
    exit(1)
EOF

RUN chmod +x /usr/local/bin/verify-talib

# Switch to vscode user
USER vscode

# Set up shell configuration
RUN echo 'export TA_INCLUDE_PATH=/usr/local/include' >> ~/.bashrc && \
    echo 'export TA_LIBRARY_PATH=/usr/local/lib' >> ~/.bashrc && \
    echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc

# Set default command
CMD ["/bin/bash"]
