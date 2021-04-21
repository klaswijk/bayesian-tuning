import json
from functools import partial
import numpy as np
import scipy.optimize as so
from skopt import gp_minimize, dummy_minimize
from skopt.space import Space
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
            'result': (result[0].x, result[0].fun),
            'n_calls': len(result[0].x_iters),
            'random_state': result[1],
            'calls': list(zip(result[0].x_iters, result[0].func_vals)),
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

        self.runs.sort(key=lambda r: r['random_state'])

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


class ObjFunc:
    def __init__(self, func, dimensions, random_state=None):
        self.random_state = random_state
        self.prev_args = []
        self.space = Space(dimensions)
        self.func = func

    def __call__(self, args):
        c = len(list(filter(lambda x: x < 1e-8, (self.space.distance(args, p)
            for p in self.prev_args))))
        self.prev_args.append(args)
        f = partial(self.func, random_state=(10 + (c << self.random_state)))
        return f(args)


def random_search(func, dimensions, n_calls=100, random_state=None):
    """A wrapper for skopt.dummy_minimize."""
    try:
        f = ObjFunc(func, dimensions, random_state=random_state)
        return (dummy_minimize(
            f,
            dimensions,
            n_calls=n_calls,
            random_state=random_state,
            **config.random
        ), random_state)
    except Exception as e:
        import traceback
        traceback.print_exc()


def bayesian_search(func, dimensions, n_calls=100, random_state=None):
    """A wrapper for skopt.gp_minimize."""
    try:
        f = ObjFunc(func, dimensions, random_state=random_state)
        return (gp_minimize(
            f,
            dimensions,
            n_calls=n_calls,
            random_state=random_state,
            **config.bayesian
        ), random_state)
    except Exception as e:
        # TODO: Some tsp instances cause exceptions, e.g. br17.atsp
        import traceback
        traceback.print_exc()


def constant_search(func, dimensions, n_calls=100, random_state=None):
    try:
        f = ObjFunc(func, dimensions, random_state=random_state)
        y_best = np.inf
        X_best = None
        y_iters = []
        X_iters = []

        for _ in range(n_calls):
            X = config.constant['params']
            y = f(X)
            X_iters.append(X)
            y_iters.append(y)

            if y < y_best:
                y_best = y
                X_best = X

        return (so.optimize.OptimizeResult(
            x=X_best,
            fun=y_best,
            x_iters=X_iters,
            func_vals=y_iters
        ), random_state)
    except Exception as e:
        import traceback
        traceback.print_exc()
