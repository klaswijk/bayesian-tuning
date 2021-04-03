import os
import time
import re
import subprocess
import multiprocessing as mp
from sys import stdout
from functools import partial
import numpy as np
from tqdm import tqdm
import config
from Optimizer import Optimizer


def run_tuning(params):
    """Run the tuning according to the params (n_runs, n_procs etc.)"""

    if params['bayesian']:
        type = 'bayesian'
    elif params['random']:
        type = 'random'
    elif params['constant']:
        type = 'constant'

    instance_name = re.search(r"([^/]+)(?=\..?tsp)", params['tsp']).group(0)
    instance_size = re.search(r"(\d+)", instance_name).group(0)

    opt = Optimizer(
        type,
        partial(
            acotsp,
            tsp_instance=params['tsp'],
            instance_size=instance_size,
            n_iter=params['n_iterations']
        )
    )

    bar = tqdm(total=params['n_runs'], file=stdout, ascii=True)

    def record_result(result):
        opt.append_run(result)
        bar.update()

    with mp.Pool(params['n_procs']) as p:

        for i in range(params['n_runs']):
            tmp = p.apply_async(_work, args=(opt, params, i), callback=record_result)

        p.close()
        p.join()
        bar.close()

    # Save the results in ./results/<instance>/<type>-<date>-<time>.json
    path = f'./results/{instance_name}/'
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file = f'{type}-{timestr}.json'

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            raise PermissionError(f'Could not create directory {path}')

    opt.write_json(path + file)


def _work(*args):
    return args[0].run(
        config.acotsp['param_dims'],
        n_calls=args[1]['n_calls'],
        random_state=args[2]
        # args[0] is the loop index. Use this as the random state (seed)
        # to make sure that the repeated run's do not share random state
    )


def acotsp(args, tsp_instance=None, instance_size=None, n_iter=None):
    """The acotsp objective function"""
    call_args = [
        config.acotsp['path'],
        '--simple',
        '-f',
        tsp_instance,
        '-i',
        str(n_iter),
        '-m',
        instance_size,
        '--hideiter'
    ]

    for val, name in zip(args, config.acotsp['param_names']):
        call_args.append(str(name))
        call_args.append(str(val))

    p = subprocess.Popen(
        call_args,
        shell=False,
        stdout=subprocess.PIPE,
        encoding='utf8'
    ).communicate()[0]

    res = p.split()[2]  # extract the length of the tour

    return float(res)
