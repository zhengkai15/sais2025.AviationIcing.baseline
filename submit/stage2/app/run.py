
import os 
import torch 
import argparse

parser = argparse.ArgumentParser(description="Process EC data.")
parser.add_argument('--base_name', type=str, required=False, default=f'../saisdata/input')
parser.add_argument('--save_name', type=str, required=False, default=f'./output')
args = parser.parse_args()

base_name = args.base_name
save_name = args.save_name


channel = ["z50","z100","z150","z200","z250","z300","z400","z500","z600","z700","z850","z925","z1000","t50","t100","t150","t200","t250","t300","t400","t500","t600","t700","t850","t925","t1000","u50","u100","u150","u200","u250","u300","u400","u500","u600","u700","u850","u925","u1000","v50","v100","v150","v200","v250","v300","v400","v500","v600","v700","v850","v925","v1000","q50","q100","q150","q200","q250","q300","q400","q500","q600","q700","q850","q925","q1000","ciwc50","ciwc100","ciwc150","ciwc200","ciwc250","ciwc300","ciwc400","ciwc500","ciwc600","ciwc700","ciwc850","ciwc925","ciwc1000","clwc50","clwc100","clwc150","clwc200","clwc250","clwc300","clwc400","clwc500","clwc600","clwc700","clwc850","clwc925","clwc1000","crwc50","crwc100","crwc150","crwc200","crwc250","crwc300","crwc400","crwc500","crwc600","crwc700","crwc850","crwc925","crwc1000","cswc50","cswc100","cswc150","cswc200","cswc250","cswc300","cswc400","cswc500","cswc600","cswc700","cswc850","cswc925","cswc1000"]
channel_task = ['t200', 't500', 't700', 't850', 't1000', 'q200','q500', 'q700', 'q850', 'q1000', 'ciwc200','ciwc500', 'ciwc700', 'ciwc850', 'ciwc1000', 'clwc200', 'clwc500', 'clwc700', 'clwc850', 'clwc1000', 'crwc200','crwc500', 'crwc700', 'crwc850', 'crwc1000', 'cswc200','cswc500', 'cswc700', 'cswc850', 'cswc1000']
c_index = [channel.index(element) for element in channel_task]
assert len(c_index)==30, "index length should be 30"

def get_sample_input():
    file_names = os.listdir(base_name)
    file_names = [os.path.join(base_name, file_name) for file_name in file_names]
    return file_names

def inference(file_list):
    os.makedirs(save_name, exist_ok=True)
    for file_name in file_list:
        print('inference on {}'.format(file_name))
        # model = torch.load('model.pth')
        # model.eval()
        input_tensor = torch.load(file_name)
        # output = model(input_tensor)
        print(input_tensor.shape)
        output = input_tensor[..., c_index, 35:80+1, 70:140+1].clone()
        print(output.shape)
        save_path = file_name.replace(base_name, save_name)
        print(save_path)
        torch.save(output, save_path)
    return

if __name__ == "__main__":
    print('inference start')
    file_list = get_sample_input()
    # print(file_list)
    inference(file_list)
    print('inference end')
