#!/bin/sh
#SBATCH --job-name=t2t_f1
#SBATCH --output=logs/output_f1_%j.out
#SBATCH -e logs/output_f1_%j.err
#SBATCH --partition=m40-long
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBTACH --mem-per-cpu=4096

source $HOME/anaconda3/bin/activate
python analysis.py /mnt/nfs/scratch1/lingeman/pubmed_test_translation.txt /mnt/nfs/scratch1/lingeman/dev/pubmed_mesh.txt
