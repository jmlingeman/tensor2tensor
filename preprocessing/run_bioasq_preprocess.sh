#!/bin/sh
#SBATCH --job-name=t2t_prepro
#SBATCH --output=logs/output_%j.out
#SBATCH -e logs/output_%j.err
#SBATCH --partition=titanx-long
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=08:00:00
#SBTACH --mem-per-cpu=4096

source $HOME/anaconda3/bin/activate
python bioasq_preprocessing.py train /mnt/nfs/scratch1/lingeman/bioasq_train/allMeSH_2018.json
