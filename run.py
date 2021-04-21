import os
import argparse
from multiprocessing import cpu_count
from tuning import run_tuning

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--random', action='store_true', help='use Random Search')
    group.add_argument('--bayesian', action='store_true', help='use Bayesian Search')
    group.add_argument('--constant', action='store_true', help='use constant parameters')
    parser.add_argument('-t', '--tsp',
        help='the path of the TSPLIB instance to run',
        required=True
    )
    parser.add_argument('-i', '--n_iterations',
        help='the number of acotsp iterations to run',
        type=int,
        required=True
    )
    parser.add_argument('-c', '--n_calls',
        help='the number of acotsp calls that the optimization function makes',
        type=int,
        required=True
    )
    parser.add_argument('-n', '--n_runs',
        help='the number of repeated runs',
        type=int,
        required=True
    )
    parser.add_argument('-p', '--n_procs',
        help='the number of processes to run (default: #cores)',
        type=int,
        default=cpu_count()
    )
    parser.add_argument('--cache',
        help='use intial sampling from given results as a cache (bayesian only)',
        type=str,
        default=None
    )
    args = parser.parse_args()
    assert(os.path.exists(args.tsp))
    run_tuning(vars(args))
