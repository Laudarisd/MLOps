# Triton Model Repository Structure Example

Place your exported models here following this structure:

```
model_repository/
  my_model/
    1/
      model.onnx
    config.pbtxt
  another_model/
    1/
      model.savedmodel
    config.pbtxt
```

- Each model has its own folder.
- Each version is a subfolder (e.g., `1/`).
- `config.pbtxt` describes the model inputs/outputs and settings.

See [Triton Model Repository documentation](https://github.com/triton-inference-server/server/blob/main/docs/model_repository.md) for details.
