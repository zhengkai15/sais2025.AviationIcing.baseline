
import os 
import torch 
import argparse

parser = argparse.ArgumentParser(description="Process EC data.")
parser.add_argument('--base_name', type=str, required=False, default=f'../tcdata/input')
parser.add_argument('--save_name', type=str, required=False, default=f'./output')
args = parser.parse_args()

base_name = args.base_name
save_name = args.save_name

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
        output = input_tensor[:, :, -1].clone()
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
