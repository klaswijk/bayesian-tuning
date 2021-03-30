#!/usr/bin/env/python3


acotsp = {
    # Path to an acotsp executable
    # Make sure the file can handle the provided type of TSPLIB-files and
    # the -q parameter (https://github.com/emmyyin/libaco)
    'path': './acotsp',
    'param_names': [
        '-a',  # alpha
        '-b',  # beta
        '-r',  # rho
        '-q',  # q
    ],
    'param_dims': [
        (0.00, 3.0),  # alpha
        (0.00, 3.0),  # beta
        (0.00, 0.99),  # rho
        (0.00, 3.0),  # q
    ],
}

bayesian = {
    'acq_func': 'LCB',
    #'xi': 0.01,
    'kappa': 1.96,
    'n_initial_points': 10,
    'x0': None
}

random = {
    'x0': None
}

constant = {
    'params': [
        1,  # alpha
        1,  # beta
        0.1,  # rho
        1,  # q
    ],
}
