# Sample Dockerfile for custom Triton Inference Server deployment
FROM nvcr.io/nvidia/tritonserver:23.09-py3

# (Optional) Copy your model repository into the image
# COPY model_repository /models

# (Optional) Install extra Python packages if needed
# RUN pip install -U pip && pip install <your-packages>

# Expose Triton ports
EXPOSE 8000 8001 8002

# Default command
CMD ["tritonserver", "--model-repository=/models"]
