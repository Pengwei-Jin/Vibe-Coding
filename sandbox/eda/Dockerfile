# ============================================================
# Qwen Code EDA Base Image (基于 Rocky Linux 9)
# ============================================================
# 此镜像仅提供 Rocky Linux 9 基础环境和 EDA 工具依赖。
# qwen-code 通过挂载宿主机目录在运行时提供，无需重新构建镜像。
#
# 构建命令:
#   docker build -f Dockerfile.base -t qwen-eda-base:rocky9 .
# ============================================================

FROM rockylinux:9

# 设置环境变量避免交互式提示
ENV TZ=Asia/Shanghai

# ============================================================
# 安装系统依赖
# ============================================================
RUN dnf install -y epel-release && \
    dnf config-manager --set-enabled crb && \
    dnf config-manager --set-enabled devel && \
    dnf update -y --allowerasing && \
    dnf install -y --allowerasing \
        # 基础工具
        bash \
        coreutils \
        procps-ng \
        psmisc \
        lsof \
        which \
        less \
        man-db \
        # EDA 工具依赖 (VCS/Verdi/DC 常用)
        redhat-lsb-core \
        time \
        tcsh \
        csh \
        ksh \
        perl \
        perl-Data-Dumper \
        gawk \
        sed \
        grep \
        file \
        hostname \
        net-tools \
        numactl \
        # 开发工具 (EDA 工具编译需要)
        gcc \
        gcc-c++ \
        make \
        cmake \
        autoconf \
        automake \
        libtool \
        # 系统库 (EDA 工具运行时依赖)
        glibc \
        glibc-devel \
        libstdc++ \
        libstdc++-devel \
        zlib \
        zlib-devel \
        ncurses \
        ncurses-libs \
        ncurses-devel \
        ncurses-compat-libs \
        readline \
        readline-devel \
        libnsl \
        # X11/图形库 (Verdi GUI 需要)
        libX11 \
        libX11-devel \
        libXext \
        libXext-devel \
        libXtst \
        libXtst-devel \
        libXrender \
        libXrender-devel \
        libXft \
        libXft-devel \
        libpng \
        libpng-devel \
        libjpeg \
        libjpeg-devel \
        libtiff \
        libtiff-devel \
        freetype \
        freetype-devel \
        fontconfig \
        fontconfig-devel \
        # 32位兼容库 (部分 EDA 工具需要)
        glibc.i686 \
        libstdc++.i686 \
        libgcc.i686 \
        # 网络工具
        curl \
        wget \
        bind-utils \
        socat \
        # 文件处理
        unzip \
        zip \
        rsync \
        # 实用工具
        jq \
        bc \
        ripgrep \
        ca-certificates \
        # Git
        git \
        # Python3
        python3 \
        python3-pip \
        python3-devel \
        # 其他常用工具
        diffutils \
        findutils \
        tar \
        gzip \
        bzip2 \
        xz \
        patch \
    && dnf clean all \
    && rm -rf /var/cache/dnf

# ============================================================
# 安装 Node.js 20 (使用 NodeSource 仓库)
# ============================================================
RUN curl -fsSL https://rpm.nodesource.com/setup_20.x | bash - && \
    dnf install -y nodejs && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# ============================================================
# 安装 GitHub CLI (gh)
# ============================================================
RUN dnf install -y 'dnf-command(config-manager)' && \
    dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    dnf install -y gh && \
    dnf clean all \
    && rm -rf /var/cache/dnf

# ============================================================
# 设置 npm 全局包目录 (qwen-code 将安装在这里)
# ============================================================
RUN mkdir -p /usr/local/share/npm-global
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin

# ============================================================
# EDA 工具环境变量
# ============================================================
# VCS (Verilog Compiler Simulator)
ENV VCS_HOME=/tools/software/synopsys/vcs/V-2023.12-SP2
# Verdi (Debug and Analysis)
ENV VERDI_HOME=/tools/software/synopsys/verdi/V-2023.12-SP2
# Design Compiler
ENV DC_HOME=/tools/software/synopsys/syn/V-2023.12-SP5
# DesignWare
ENV DESIGNWARE_HOME=/tools/software/synopsys/vip/V-2023.12

# 将 EDA 工具的 bin 目录加入 PATH
ENV PATH=$PATH:$VCS_HOME/bin:$VERDI_HOME/bin:$DC_HOME/bin:$DESIGNWARE_HOME/bin

# 设置 Synopsys License 变量
ENV SNPSLMD_LICENSE_FILE=27000@localhost.localdomain

# ============================================================
# 创建工作目录
# ============================================================
WORKDIR /workspace

# 默认入口点 (实际运行时由 start.sh 覆盖)
CMD ["bash"]
