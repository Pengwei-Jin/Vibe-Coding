# EDA Sandbox

Docker-based sandbox for safely running EDA tools (VCS, Verdi, Design Compiler) under Qwen Code YOLO mode.

Based on Rocky Linux 9, with all system dependencies pre-installed. Qwen Code is mounted from the host at runtime — no image rebuild needed when upgrading.

## Quick Start

```bash
# Build the image
docker build -t qwen-eda-rockylinux:9.7 .

# Launch sandbox
./start.sh                   # interactive mode
./start.sh "your prompt"     # with initial prompt
```

## ⚠️ EDA Environment Variables — Must Customize

The Dockerfile contains EDA tool paths and license settings that are **specific to the original author's environment**. You **must** modify them to match your own setup before building.

The relevant section in `Dockerfile`:

```dockerfile
# VCS (Verilog Compiler Simulator)
ENV VCS_HOME=/tools/software/synopsys/vcs/V-2023.12-SP2
# Verdi (Debug and Analysis)
ENV VERDI_HOME=/tools/software/synopsys/verdi/V-2023.12-SP2
# Design Compiler
ENV DC_HOME=/tools/software/synopsys/syn/V-2023.12-SP5
# DesignWare
ENV DESIGNWARE_HOME=/tools/software/synopsys/vip/V-2023.12

# License server
ENV SNPSLMD_LICENSE_FILE=27000@localhost.localdomain
```

Update each variable to point to your actual tool installation paths and license server address.

Similarly, `start.sh` contains an `IMAGE_NAME` and a host mount path (`/tools`) that may need adjustment:

```bash
IMAGE_NAME="qwen-eda-rockylinux:9.7"
SANDBOX_FLAGS="-v /tools:/tools:ro --network host ..."
```
