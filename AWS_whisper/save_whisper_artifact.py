### PyTorch
import whisper
import torch
# Load the PyTorch model and save it in the local repo
model = whisper.load_model("base")
torch.save(
    {
        'model_state_dict': model.state_dict(),
        'dims': model.dims.__dict__,
    },
    'base.pt'
)