FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Avoid interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
# Python 3.10 is default in Ubuntu 22.04
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    cmake \
    tshark \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Install ttyd (Web Terminal)
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.7.4/ttyd.x86_64 -O /usr/bin/ttyd && \
    chmod +x /usr/bin/ttyd

WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
# Upgrade pip first
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose web terminal port
EXPOSE 7681

# Create a non-root user
RUN useradd -m houdinis
RUN chown -R houdinis:houdinis /app
USER houdinis

# Command to run ttyd serving the Houdinis CLI
CMD ["ttyd", "--port", "7681", "--writable", "python3", "main.py", "--console"]
