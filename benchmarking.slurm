#!/bin/bash -l
#SBATCH --account=lp_dreesenlab
#SBATCH --clusters=wice
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=3
#SBATCH --time=01:00:00
#SBATCH --job-name=benchmarking.py
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=luong.vuong@uhasselt.be

module load Python/3.13.1-GCCcore-14.2.0
pip install --user matplotlib

python3 benchmarking.py
