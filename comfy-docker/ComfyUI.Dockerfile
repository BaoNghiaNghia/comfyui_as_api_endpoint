# Use the official Rocky Linux base image
FROM rockylinux/rockylinux:latest

RUN dnf -y install bash epel-release && \
    dnf clean all

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/dnf \
    set -eu \
    && dnf install -y --setopt=install_weak_deps=False \
        python3.11 python3.11-pip python3.11-devel \
        python3.11-wheel python3.11-setuptools python3.11-numpy \
        gcc gcc-c++ shadow-utils git ca-certificates \
        mesa-libGL glib2 ncdu nmap dos2unix \
        aria2 findutils \
    && rm -rf /usr/lib/python3.*/site-packages/EXTERNALLY-MANAGED

# Fix for libs (.so files), adjusting paths as necessary for Rocky Linux
# Note: The Python version in the path should be adjusted based on the installed Python version
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib64/python3.*/site-packages/torch/lib"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/python3.*/site-packages/nvidia/cufft/lib"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/python3.*/site-packages/nvidia/cuda_runtime/lib"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/lib/python3.*/site-packages/nvidia/cuda_cupti/lib"

ENV HF_HOME="/ComfyUIDocker/HFCache"

# Ensure pip is up to date
RUN pip3 install --upgrade pip

# Install specific packages with version constraints and custom indexes
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install mpmath==1.3.0 --pre -U xformers optimum optimum[onnxruntime-gpu] ultralytics \
        --index-url https://download.pytorch.org/whl/cu121 \
        --extra-index-url https://pypi.org/simple

EXPOSE 8189
ENV CLI_ARGS=""

CMD ["bash","/ComfyUIDocker/Scripts/Initial.sh"]
