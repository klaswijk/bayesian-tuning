import subprocess
import multiprocessing as mp
from sys import stdout
from os import getpid
from functools import partial
import numpy as np
from tqdm import tqdm
import config
from Optimizer import Optimizer


def run_tuning(params):
    """Run the tuning according to the params (n_runs, n_procs etc.)"""

    type = 'bayesian' if params['bayesian'] else 'random'
    opt = Optimizer(type)
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

    opt.write_json(f"./results/{type}/result.json")  # TODO: Unique name


def _work(*args):
    func = partial(_acotsp, args[1]['tsp'], args[1]['n_iterations'])
    return args[0].run(
        func,
        config.acotsp['param_dims'],
        n_calls=args[1]['n_calls'],
        random_state=args[2]
        # args[0] is the loop index. Use this as the random state (seed)
        # to make sure that the repeated run's do not share random state
    )


def _acotsp(tsp, iter, args):
    """The acotsp objective function"""
    call_args = [
        config.acotsp['path'],
        '--simple',
        '-f',
        tsp,
        '-i',
        str(iter)
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
