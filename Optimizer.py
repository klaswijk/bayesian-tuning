import json
import numpy as np
import scipy.optimize as so
from skopt import gp_minimize

class Optimizer:
    """Wraps an optimization function to record partial results"""

    def __init__(self, optimization_func):
        optimization_funcs = {
            'random': random_search,
            'bayesian': bayesian_search,
        }
        self.run = optimization_funcs[optimization_func]

        self.results = {
            'optimizer': str(self.run),  # TODO: Improve
            'n_runs': 0,
            'runs': [],
        }

    def append_run(self, result):
        run = {
            'result': (result.x, result.fun),
            'n_iterations': len(result.x_iters),
            'iterations': list(zip(result.x_iters, result.func_vals)),
        }
        self.results['runs'].append(run)
        self.results['n_runs'] += 1

    def write_json(self, path):
        """
        Write results to a JSON-file, including information about the
        optimizer used.
        """
        with open(path, 'w') as f:
            json.dump(self.results, f)


def random_search(func, dimensions, n_calls=100, random_state=None):
    """A naive Random Search for Black-Box Optimization"""
    rng = np.random.default_rng(random_state)

    y_best = np.inf
    X_best = None

    y_iters = []
    X_iters = []

    for _ in range(n_calls):
        # min is inclusive, max is exclusive
        X = [rng.uniform(low=min_val, high=max_val)
                for min_val, max_val in dimensions]
        y = func(X)

        X_iters.append(X)
        y_iters.append(y)

        if y < y_best:
            y_best = y
            X_best = X

    return so.optimize.OptimizeResult(
        x=X_best,
        fun=y_best,
        x_iters=X_iters,
        func_vals=y_iters
    )


def bayesian_search(func, dimensions, n_calls=100, random_state=None):
    """A wrapper for skopt.gp_minimize"""
    try:
        res = gp_minimize(
            func,
            dimensions,
            n_calls=n_calls,
            random_state=random_state,
        )
    except Exception as e:
        # TODO: Some tsp instances cause exceptions, e.g. br17.atsp
        import traceback
        traceback.print_exc()
    return res
