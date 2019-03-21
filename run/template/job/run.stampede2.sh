#!/bin/bash
#SBATCH --job-name={{ NAME }}
#SBATCH --partition={{ QUEUE }}
#SBATCH --nodes={{ NODES }}
#SBATCH --ntasks-per-node={{ MPI }}
#SBATCH --cpus-per-task={{ OMP }}
#SBATCH --time={{ HOUR }}:00:00
#SBATCH --account=TG-AST140023
#SBATCH --output=run.log
#SBATCH --mail-type=all
#SBATCH --workdir=.
# Reference: https://portal.tacc.utexas.edu/user-guides/stampede2#job-scripts
set -e
cd ..
pwd
source "$GIZENV_ACTIVATE"

export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
OPT="tacc_affinity"

date
if [[ -d output/restartfiles ]]; then
    # Restart
    ibrun $OPT ./GIZMO gizmo_params.txt 1
else
    # Start from scratch
    ibrun $OPT ./GIZMO gizmo_params.txt
fi
date