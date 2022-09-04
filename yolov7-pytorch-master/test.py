import torch
print(torch.version)
print(torch.cuda.is_available())#要為True
print(torch.version.cuda)
print(torch.backends.cudnn.version())