#!/usr/bin/env python
"""Select halos from the box for zoom-in runs.

Before this step, make sure data/box/L86/output/snapdir_005/ is available.
"""
from toolbox.env import repo_dir
from toolbox.job import BridgesJob


snap_file = repo_dir / 'data/box/L86/output/snapdir_005/snapshot_005.0.hdf5'
ahf_dir = repo_dir / 'data/box-halo/ahf'
cand_file = repo_dir / 'data/box-halo/candidates.csv'

job_ahf_setup = BridgesJob(
    'ahf-setup',
    f'ahf-setup.py -s {snap_file} -w {ahf_dir} -c 16',  # 16 = 4 * (28 / 7)
    nodes=1, ncpus=1, time='1:00:00',
)
if not (ahf_dir / 'snapshot_005.input').exists():
    id_ahf_setup = job_ahf_setup.submit()
else:
    id_ahf_setup = None

job_ahf_run = BridgesJob(
    'ahf-run',
    'AHF-dmo-mpi snapshot_005.input',
    run_dir=ahf_dir,
    nodes=4, ncpus=7, time='1:00:00', mpi=True,
)
if not (ahf_dir / 'snapshot_005.parameter').exists():
    id_ahf_run = job_ahf_run.submit(depend=id_ahf_run)
else:
    id_ahf_run = None

job_select_cand = BridgesJob(
    'select-cand',
    f'select-cand.py -s {snap_file} -h {ahf_dir} -o {cand_file}',
    nodes=4, ncpus=4, time='2:00:00', mpi=True,
)
if not cand_file.exists():
    job_select_cand.submit(depend=id_ahf_run)
