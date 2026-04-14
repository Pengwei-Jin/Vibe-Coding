#!/bin/bash
# ============================================================
# Qwen Code EDA Sandbox 启动脚本 (挂载宿主机 npm 全局 qwen)
# ============================================================
# 使用条件:
#   宿主机已通过 nvm + npm install -g @qwen-code/qwen-code 安装了 qwen
#
# 更新 qwen 只需在宿主机运行:
#   npm update -g @qwen-code/qwen-code
#
# 无需重新构建 docker image。
#
# 使用方法:
#   ./start-new.sh                    # 交互模式启动
#   ./start-new.sh "your prompt"       # 带提示词启动
# ============================================================

# 镜像名称
IMAGE_NAME="qwen-eda-rockylinux:9.7"

# 宿主机 nvm node 目录
# qwen 安装在: $NODE_DIR/bin/qwen 和 $NODE_DIR/lib/node_modules/@qwen-code/qwen-code
NODE_DIR="$(nvm which current 2>/dev/null | xargs dirname | xargs dirname)"
if [ -z "$NODE_DIR" ] || [ ! -d "$NODE_DIR" ]; then
    # 如果 nvm 命令不可用，使用当前 node 路径推导
    NODE_DIR="$(which node | xargs dirname | xargs dirname)"
fi

if [ -z "$NODE_DIR" ] || [ ! -d "$NODE_DIR" ]; then
    echo "错误: 找不到 nvm node 目录"
    exit 1
fi

echo "=> 使用宿主机 node: $NODE_DIR"

# Sandbox 挂载选项
# - /tools: EDA 工具安装目录 (只读挂载)
# - --network host: 使用宿主机网络
# - nvm node 目录: 挂载宿主机 node 全局包 (包含 qwen) 到容器内相同路径
SANDBOX_FLAGS="-v /tools:/tools:ro --network host -v $NODE_DIR:/usr/local/share/npm-global:ro"

# 检查镜像是否存在
if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
    echo "错误: 镜像 $IMAGE_NAME 不存在"
    echo "请先构建镜像: docker build -f Dockerfile.base -t $IMAGE_NAME ."
    exit 1
fi

# 启动 sandbox
SANDBOX_FLAGS="$SANDBOX_FLAGS" qwen --sandbox --sandbox-image "$IMAGE_NAME" --yolo "$@"
