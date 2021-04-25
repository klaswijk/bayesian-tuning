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
        (1.0, 5.0),  # alpha
        (0.0, 4.0),  # beta
        (0.1, 0.99),  # rho
        (0.0, 10.0),  # q
    ],
}

bayesian = {
    'acq_func': 'PI',
    'xi': 0.01,  # EI and PI
    #'kappa': 1.96,  # LCB
    'n_initial_points': 25,
    'initial_point_generator': 'hammersly',
    'noise': 0.07,
}

random = {
    'initial_point_generator': 'random',
}

constant = {
    'params': [
        1,  # alpha
        1,  # beta
        0.1,  # rho
        1,  # q
    ],
}
