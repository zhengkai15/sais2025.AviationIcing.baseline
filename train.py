import os
import sys
import time
from tqdm import tqdm
import argparse
from distutils.util import strtobool
from deeptools.utils import create_logger, get_color_codes
from deeptools.config import load_yaml, print_config, update_config_from_args, set_random_seed,save_yaml
from deeptools.model import get_model
from deeptools.train import get_optim,get_scheduler,get_early_stopping, train_epoches, eval_epoches, plot_metrics, update_tqdm
from deeptools.dataloader import get_dataloader
from deeptools.loss import get_loss

BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_RESET = get_color_codes()

def parse_args():
    """Parse command line arguments for model training configuration."""
    parser = argparse.ArgumentParser(
        description="Parse configuration arguments."
    )
    
    # verbose
    parser.add_argument(
        "--debug.verbose",
        type=lambda x: bool(strtobool(x)), 
        default=False)
    
    # config
    parser.add_argument(
        '--config',
        type=str,
        default='./conf/config.yaml',
    )
    
    # config
    parser.add_argument(
        '--lr.value',
        type=float,
        default=0.0001,
    )
    
    # config
    parser.add_argument(
        '--lr.scheduler.min_lr',
        type=float,
        default=0.00005,
    )
    
    # exp.dir
    parser.add_argument(
        '--exp.dir',
        type=str,
        default='./exp/debug',
        help=''
    )
    return parser.parse_args()



def main():
    # args
    args = parse_args()
    config_path = args.config
    
    # config 
    config = load_yaml(file_path=config_path)
    config = update_config_from_args(config=config, args=args)
    exp = config["exp"]["dir"]

    # log
    if vars(args)["debug.verbose"]:
        log_path=None 
    else:
        log_path= exp
    logger = create_logger(log_level="DEBUG", log_path=log_path)
    

    print_config(config)
    
    # seed 
    set_random_seed(config["seed"]["random_seed"])
    
    # env config 
    os.environ['CUDA_VISIBLE_DEVICES'] = config["env"]["gpus_id"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    # model
    model = get_model(config=config)
    logger.info(model)
    total_params = sum(p.numel() for p in model.parameters()) / 1e9
    logger.info(f"{BG_RED} Total parameters: {total_params} Billion {BG_RESET}")
    
    # test model
    import torch
    x = torch.randn([1, 2, 117, 181, 360]) 

    y = model(x)
    print(x.shape, y.shape)  
    # optim 
    optimizer = get_optim(config=config, model=model)
    logger.info(optimizer)
    
    # schduler
    scheduler = get_scheduler(config=config, optimizer=optimizer)
    logger.info(scheduler)
    # earlystoping
    early_stopping = get_early_stopping(config=config)
    logger.info(early_stopping)
    
    # # from deeptools.datasets.dataset import mydataset  # demo dataloader
    from dataset.era5 import ERA5 as mydataset
    
    train_loader, train_loader_eval, valid_loader, test_loader = get_dataloader(config, mydataset=mydataset)  

    # loss
    loss_func=get_loss(config)
    logger.info(loss_func)

    model.cuda()
    # save_yaml
    save_yaml(config=config)
    # train 
    for epoch in range(config["train"]["start_epoch"], config["train"]["num_epochs"]):
        with tqdm(total=config["train"]["iter_num"], desc=f'trainning epoch:{epoch}') as pbar:
            last_update_time = time.time()  # 记录上次更新时间
            for index, (ft_item, gt_item, _) in enumerate(train_loader):
                ft_item,gt_item = ft_item.cuda().float(), gt_item.cuda().float()
                
                output_item = model(ft_item)
                # calculate loss
                loss = loss_func(output_item, gt_item)
                
                logger.info(f"{loss.item()}")
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                # update qtdm
                last_update_time = update_tqdm(total_num=len(train_loader), index=index, pbar=pbar, last_update_time=last_update_time, update_type='by_time')

if __name__ == "__main__":
    main()
    