# Sample Python client for Triton Inference Server
import tritonclient.http as httpclient
import numpy as np

# Connect to Triton server
client = httpclient.InferenceServerClient(url="localhost:8000")

# Example: Prepare input data (adjust for your model)
input_data = np.random.rand(1, 3, 224, 224).astype(np.float32)
inputs = [httpclient.InferInput("input", input_data.shape, "FP32")]
inputs[0].set_data_from_numpy(input_data)

# Prepare output
outputs = [httpclient.InferRequestedOutput("output")]

# Run inference
results = client.infer(model_name="my_model", inputs=inputs, outputs=outputs)

# Get output data
output_data = results.as_numpy("output")
print("Output:", output_data)
