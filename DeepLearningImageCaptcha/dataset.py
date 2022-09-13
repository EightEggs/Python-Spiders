import os
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from PIL import Image
import encoding as ohe
import setting


class mydataset(Dataset):

    def __init__(self, folder, transform=None):
        self.train_image_file_paths = [os.path.join(
            folder, image_file) for image_file in os.listdir(folder)]
        self.transform = transform

    def __len__(self):
        return len(self.train_image_file_paths)

    def __getitem__(self, idx):
        image_root = self.train_image_file_paths[idx]
        image_name = image_root.split(os.path.sep)[-1]
        image = Image.open(image_root)
        if self.transform is not None:
            image = self.transform(image)
        label = ohe.encode(image_name.split('_')[0])
        return image, label


transform = transforms.Compose([
    transforms.ColorJitter(),
    transforms.ToTensor(),
    transforms.Grayscale(1),
    transforms.Normalize(mean=0.5, std=0.5)
])


def get_train_data_loader():
    dataset = mydataset(setting.TRAIN_DATASET_PATH, transform=transform)
    return DataLoader(dataset, batch_size=64, num_workers=4, shuffle=True)


def get_eval_data_loader():
    dataset = mydataset(setting.EVAL_DATASET_PATH, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=True)


def get_predict_data_loader():
    dataset = mydataset(setting.PREDICT_DATASET_PATH, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=True)
