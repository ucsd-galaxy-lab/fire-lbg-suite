#!/usr/bin/env bash
#PBS -N candidate-selection
#PBS -q condo
#PBS -l nodes=4:ppn=16:ib
#PBS -l walltime=8:00:00
#PBS -j oe
#PBS -o candidate-selection.log
#PBS -V
#PBS -d .
set -e
source "$PROJECT_ACTIVATE"
cd ..
echo "$PWD"

date
export OMP_NUM_THREADS=4
mpirun -v -machinefile $PBS_NODEFILE -npernode 4 \
-x PATH -x LD_LIBRARY_PATH -x OMP_NUM_THREADS \
./select-candidate.py
date
