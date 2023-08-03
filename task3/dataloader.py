import torchvision.transforms as transforms

from torch.utils.data import Dataset


class ImagesDataset(Dataset):
    RESCALE_SIZE = 50

    def __init__(self, file):
        super().__init__()
        self.file = file

    def __len__(self):
        return 1

    def __getitem__(self, index):
        transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize(size=(self.RESCALE_SIZE, self.RESCALE_SIZE)),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

            ])
        x = transform(self.file)
        return x
