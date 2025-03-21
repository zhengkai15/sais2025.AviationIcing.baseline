from dataset.era5 import ERA5
from deepsuit.utils import time_me
from torch.utils.data import Dataset, DataLoader

def create_dataloaders(config):
    train_dataset = ERA5(flag='train', config=config)
    train_loader = DataLoader(train_dataset, batch_size=4, num_workers=0, pin_memory=True, shuffle=True)

    val_dataset = ERA5(flag='test', config=config)
    val_loader = DataLoader(val_dataset, batch_size=4, num_workers=0, pin_memory=True, shuffle=False)
    return train_loader, val_loader


def main():
    import yaml
    yaml_file_path = "/cpfs01/projects-HDD/cfff-4a8d9af84f66_HDD/public/zhengkai/zhengkai_dev/sais2025.baseline/conf/config.yaml"
    with open(yaml_file_path, "r") as f:
        config = yaml.safe_load(f)

    train_loader, val_loader = create_dataloaders(config)
    # val_loader = create_dataloaders(config)

    from deepsuit.utils import print_variable_info
    for index, (ft_item, gt_item, _) in enumerate(train_loader):
        # _, ft_item,gt_item  = data["times"], data["inputs"],data["targets"]
        print_variable_info({"ft":ft_item, "gt":gt_item, "_":_})
        # break

    for index, (ft_item, gt_item, _) in enumerate(val_loader):
        # _, ft_item,gt_item  = data["times"], data["inputs"],data["targets"]
        print_variable_info({"ft":ft_item, "gt":gt_item, "_":_})
        break


if __name__ == "__main__":
    main()
    