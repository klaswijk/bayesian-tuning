import json
from functools import partial
import numpy as np
import scipy.optimize as so
from skopt import gp_minimize
import config

class Optimizer:
    """Wraps an optimization function to record partial results."""

    def __init__(self, optimization_func, objective_func):
        name_to_func = {
            'random': random_search,
            'bayesian': bayesian_search,
            'constant': constant_search,
        }
        self.optimization_func_name = optimization_func
        self.run = partial(name_to_func[self.optimization_func_name], objective_func)
        self.runs = []


    def append_run(self, result):
        """
        Add the run to self.results. All runs are assumed to come
        from the same optimizer run on the same function.
        """
        run = {
            'result': (result.x, result.fun),
            'n_calls': len(result.x_iters),
            'calls': list(zip(result.x_iters, result.func_vals)),
        }
        self.runs.append(run)


    def write_json(self, path):
        """
        Write results to a JSON-file, including information about the
        optimizer used.
        """
        name_to_params = {
            'random': config.random,
            'bayesian': config.bayesian,
            'constant': config.constant,
        }
        params = name_to_params[self.optimization_func_name]

        results = {
            'optimization_function': {
                'name': self.optimization_func_name,
                'parameters': {**{'n_calls': self.runs[0]['n_calls']}, **params},
            },
            'objective_function': {
                'name': self.run.args[0].func.__name__,
                'parameters': self.run.args[0].keywords
            },
            'search_space': list(zip(config.acotsp['param_names'],
                                     config.acotsp['param_dims'])),
            'n_runs': len(self.runs),
            'runs': self.runs,
        }

        with open(path, 'w') as f:
            json.dump(results, f)


def random_search(func, dimensions, n_calls=100, random_state=None):
    """A naive Random Search for Black-Box Optimization."""
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
    """A wrapper for skopt.gp_minimize."""
    try:
        res = gp_minimize(
            func,
            dimensions,
            n_calls=n_calls,
            random_state=random_state,
            **config.bayesian
        )
    except Exception as e:
        # TODO: Some tsp instances cause exceptions, e.g. br17.atsp
        import traceback
        traceback.print_exc()
    return res


def constant_search(func, dimensions, n_calls=100, random_state=None):
    return random_search(
        func,
        [(p, p) for p in config.constant['params']],
        n_calls=n_calls,
        random_state=random_state
    )
