import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np

class LggMriDataset(Dataset):
    def __init__(self, image_mask_pairs, transform=None):
        self.image_mask_pairs = image_mask_pairs
        self.transform = transform

    def __len__(self):
        return len(self.image_mask_pairs)

    def __getitem__(self, index):
        img_path, mask_path = self.image_mask_pairs[index]
        
        image = np.array(Image.open(img_path).convert("RGB"))
        mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
        
        mask[mask == 255.0] = 1.0

        if self.transform is not None:
            augmentations = self.transform(image=image, mask=mask)
            image = augmentations["image"]
            mask = augmentations["mask"]

        return image, mask