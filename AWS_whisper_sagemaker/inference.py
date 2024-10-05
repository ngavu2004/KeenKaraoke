import torch
import whisper
import os
### PyTorch
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def model_fn(model_dir):
    """
    Load and return the model
    """
    model = whisper.load_model(os.path.join(model_dir, 'base.pt'))
    model = model.to(DEVICE)
    return model