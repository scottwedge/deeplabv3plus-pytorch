''' 
    Main script for training segmentation models with pytorch lightning
'''
from segmentation_arguments import get_training_arguments
from segmentation_trainer import SegmentationTrainer
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint


def main():
    args = get_training_arguments()
    format_arguments(args)
    mode = get_training_mode(args)

    trainer = Trainer(
        accumulate_grad_batches=args.accumulate_grad_batches,
        check_val_every_n_epoch=args.val_interval,
        default_root_dir=args.ckpt_path,
        max_epochs=args.num_epochs,
        early_stop_callback=False,
        distributed_backend=mode,
        amp_level=args.amp_level,
        weights_summary=None,
        auto_lr_find=False,
        gpus=args.gpus,
    )

    model = SegmentationTrainer(args)
    trainer.fit(model)

def format_arguments(args):
    # Lightning Modules can't store None
    args.val_interval = 1 if args.val_interval is None else args.val_interval
    args.ckpt_path = None if args.ckpt_path == 'None' else args.ckpt_path

def get_training_mode(args):
    return 'ddp' if len(args.gpus) > 1  else None

if __name__ == '__main__':
    main()