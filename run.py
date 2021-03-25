import os
import argparse
from multiprocessing import cpu_count
from tuning import run_tuning

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--random', action='store_true')
    group.add_argument('-b', '--bayesian', action='store_true')
    parser.add_argument('-t', '--tsp',
        help='The path of the TSPLIB instance to run',
        required=True
    )
    parser.add_argument('-i', '--n_iterations',
        help='The number of acotsp iterations to run',
        type=int,
        required=True
    )
    parser.add_argument('-c', '--n_calls',
        help='The number of acotsp calls that the optimization function makes',
        type=int,
        required=True
    )
    parser.add_argument('-n', '--n_runs',
        help='The number of repeated runs',
        type=int,
        required=True
    )
    parser.add_argument('-p', '--n_procs',
        help='The number of processes to run in parallell (default: #cores)',
        type=int,
        default=cpu_count()
    )
    args = parser.parse_args()
    assert(os.path.exists(args.tsp))
    run_tuning(vars(args))
