# hash:sha256:08a389c93c03f0f8f1a5f37303a176d1d8a81414fe73704b036d0ec96be3d0f6
FROM registry.codeocean.com/codeocean/pytorch:2.1.0-cuda11.8.0-mambaforge23.1.0-4-python3.10.12-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sumo=1.12.0+dfsg1-1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U --no-cache-dir \
    matplotlib==3.9.1 \
    osmnx==1.9.3 \
    scikit-learn==1.5.1 \
    sumolib==1.20.0 \
    tensorboard==2.17.0 \
    traci==1.20.0
