import xarray as xr
import pandas as pd
import sys
import os
import json
import yaml
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
from matplotlib import font_manager
from copy import deepcopy
from torch.utils.data import DataLoader, Dataset
import torch

class ERA5(Dataset):
    def __init__(self, config, flag="train"):
        self.data_dict = dict(
            z='geopotential',
            t='temperature',
            u='u_component_of_wind',
            v='v_component_of_wind',
            q='specific_humidity',
            ciwc='specific_cloud_ice_water_content',
            clwc='specific_cloud_liquid_water_content',
            crwc='specific_rain_water_content',
            cswc='specific_snow_water_content',
        )
        
        self.data_path = config["data"]["data_path"]
        self.datetimes = config["data"][f"datetimes_{flag}"]
        self.start_time = pd.to_datetime(self.datetimes[0], format="%Y%m%d%H")
        self.end_time = pd.to_datetime(self.datetimes[1], format="%Y%m%d%H")
        self.selected_levels = config["data"]["selected_levels"]
        
        self.dataset = self._load_data()
        self.in_frames = config["data"]["in_frames"]
        self.out_frames = config["data"]["out_frames"]
        
        times = self.dataset.time.values
        self.times = np.array([t for t in times if (t >= self.start_time and t <= self.end_time)])
        self.init_times = self.times[slice(self.in_frames, -self.out_frames)]
        self.num_data = len(self.init_times)
        
    def _load_data(self):
        dataset = []
        date_range = pd.date_range(start=self.start_time, end=self.end_time, freq='D')
        
        for date in date_range:
            date_str = date.strftime('%Y%m%d')
            year = date.strftime('%Y')
            ds_date = []
            for short, long in self.data_dict.items():
                file_path = os.path.join(self.data_path, long, year, f"{date_str}.nc")
                if not os.path.exists(file_path):
                    logger.warning(f"文件不存在: {file_path}")
                    continue
                    
                ds = xr.open_mfdataset(file_path)
                ds = ds.rename({
                    'pressure_level': 'level',
                    'valid_time': 'time',
                    'latitude': 'lat',
                    'longitude': 'lon'
                })

                # 重命名变量为z50...形式
                for level in self.selected_levels:
                    var_name = f'{short}{level}'
                    level_da = ds[short].sel(level=level).drop_vars('level')
                    level_da = level_da.assign_coords(level = var_name).expand_dims(dim='level')
                    ds_date.append(level_da)
            ds_date = xr.concat(ds_date, dim='level').transpose('time', 'level', 'lat', 'lon')
            dataset.append(ds_date)
            
        dataset = xr.concat(dataset, dim='time')
        if 'expver' in dataset.coords:
            dataset = dataset.drop_vars('expver')
        dataset = dataset.to_dataset(name='data')
        return dataset

    def __len__(self):
        return self.num_data

    def __getitem__(self, idx):
        inds = np.arange(idx, idx+self.in_frames+self.out_frames)
        in_frames_inds = inds[:self.in_frames]
        out_frames_inds = inds[self.in_frames:]
        all_frames_inds = np.concatenate([in_frames_inds, out_frames_inds])
        all_frames = self.dataset.sel(time=self.times[all_frames_inds])
        imgs = torch.from_numpy(all_frames.data.values)
        imgs = torch.nan_to_num(imgs) # t c h w 
        inputs = imgs[:self.in_frames]
        targets = imgs[self.in_frames:]
        
        times = self.times[all_frames_inds] 
        init_time = pd.to_datetime(times[self.in_frames-1]).strftime("%Y%m%d%H")
        return inputs, targets, init_time

if __name__ == "__main__":
    config_path = "/cpfs01/projects-HDD/cfff-4a8d9af84f66_HDD/public/shundai/shundai_dev/sais2025.baseline/conf/config_ds.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    era5_dataset = ERA5(config, flag="train")
    dataloader = DataLoader(era5_dataset, batch_size=16, num_workers=16, shuffle=False)
    print(era5_dataset[0])
