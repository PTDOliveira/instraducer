FROM continuumio/miniconda3:24.7.1-0

# Create env
RUN conda update -n base -c defaults conda -y && \
    conda create -n app python=3.12 -y && \
    conda clean -afy

# Install packages
# torch CPU wheels via conda-forge are stable; add others via pip
RUN /bin/bash -lc "source activate app && \
    pip install --no-cache-dir \
        flask \
        torch \
        transformers \
        accelerate"

# Download the model
RUN conda run -n app python -c "from transformers import pipeline; pipeline(\"text-generation\", model=\"Unbabel/Tower-Plus-2B\", device_map=\"auto\")"

WORKDIR /app

# Copy your script and model
COPY translate.py /app/translate.py

ENV FLASK_APP=translate.py

EXPOSE 2375

# Use conda-run to avoid manual activation in ENTRYPOINT
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "app", "flask", "run", "--host=0.0.0.0", "--port=2375"]