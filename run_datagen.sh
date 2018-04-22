#!/bin/sh
#SBATCH --job-name=t2t_datagen
#SBATCH --output=logs/output_%j.out
#SBATCH -e logs/output_%j.err
#SBATCH --partition=titanx-short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00
#SBTACH --mem-per-cpu=4096

module add cuda80/toolkit
module add cuda80/blas
source $HOME/anaconda3/bin/activate
python ./tensor2tensor/bin/t2t_datagen.py --problem=translate_pubmed --data_dir=/mnt/nfs/scratch1/lingeman/t2t_data --tmp_dir=/mnt/nfs/scratch1/lingeman/t2t_tmp

