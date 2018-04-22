#!/bin/sh
#SBATCH --job-name=t2t_pubmed_decode
#SBATCH --output=logs/output_decode_%j.out
#SBATCH -e logs/output_decode_%j.err
#SBATCH --partition=m40-long
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBTACH --mem-per-cpu=4096

module add cuda80/toolkit
module add cuda80/blas
module add cudnn/6.0
source $HOME/anaconda3/bin/activate

./tensor2tensor/bin/t2t-decoder --data_dir=/mnt/nfs/scratch1/lingeman/t2t_data --problems=translate_pubmed --model=transformer --hparams_set=transformer_base --decode_from_file=/mnt/nfs/scratch1/lingeman/dev/pubmed_cleaned_MINYEAR-2009.txt --decode_to_file=/mnt/nfs/scratch1/lingeman/pubmed_test_translation.txt --output_dir=/mnt/nfs/scratch1/lingeman/t2t_output

./tensor2tensor/bin/t2t-bleu --translation=/mnt/nfs/scratch1/lingeman/pubmed_test_translation.txt --reference=/mnt/nfs/scratch1/lingeman/dev/pubmed_mesh.txt

