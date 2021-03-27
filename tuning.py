import subprocess
import multiprocessing as mp
from sys import stdout
from os import getpid
import numpy as np
from tqdm import tqdm
import config
from Optimizer import Optimizer

global_params = None
opt = None

def run_tuning(params):
    """Run the tuning according to the params (n_runs, n_procs etc.)"""

    global global_params
    global_params = params

    type = 'bayesian' if global_params['bayesian'] else 'random'

    global opt
    opt = Optimizer(type)

    bar = tqdm(total=global_params['n_runs'], file=stdout, ascii=True)

    def record_result(result):
        opt.append_run(result)
        bar.update()

    with mp.Pool(global_params['n_procs']) as p:

        for i in range(global_params['n_runs']):
            tmp = p.apply_async(_work, args=(i,), callback=record_result)

        p.close()
        p.join()
        bar.close()

    opt.write_json(f"./results/{type}/result.json")  # TODO: Unique name

def _work(*args):
    return opt.run(
        _acotsp,
        config.acotsp['param_dims'],
        n_calls=global_params['n_calls'],
        random_state=args[0]
        # args[0] is the loop index. Use this as the random state (seed)
        # to make sure that the repeated run's do not share random state
    )

def _acotsp(args):
    """The acotsp objective function"""
    call_args = [
        config.acotsp['path'],
        '--simple',
        '-f',
        global_params['tsp'],
        '-i',
        str(global_params['n_iterations'])
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

    return float(p)
