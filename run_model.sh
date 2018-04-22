#!/bin/sh
#SBATCH --job-name=t2t_pubmed
#SBATCH --output=logs/output_%j.out
#SBATCH -e logs/output_%j.err
#SBATCH --partition=m40-long
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:4
#SBATCH --time=168:00:00
#SBTACH --mem-per-cpu=8192

module add cuda80/toolkit
module add cuda80/blas
module add cudnn/6.0
source $HOME/anaconda3/bin/activate
nvidia-smi
./tensor2tensor/bin/t2t-trainer --data_dir=/mnt/nfs/scratch1/lingeman/t2t_data --tmp_dir=/mnt/nfs/scratch1/lingeman/t2t_tmp --problems=translate_pubmed --model=transformer --hparams_set=transformer_base --output_dir=/mnt/nfs/scratch1/lingeman/t2t_output --train_steps=10000000 --eval_steps=1000 --hparams='batch_size=8192'

