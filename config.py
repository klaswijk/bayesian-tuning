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
        (0.50, 1.00),  # alpha
        (2.00, 4.00),  # beta
        (0.01, 0.05),  # rho
        (0.50, 1.50),  # q
    ],
}
