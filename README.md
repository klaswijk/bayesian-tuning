# bayesian-tuning
Bayesian parameter tuning of the Ant Colony Metaheuristic applied to the Travelling Salesman Problem

## How to use
1. Make sure you have both a [libaco (acotsp)](https://github.com/emmyyin/libaco) executable and one or more [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) intance(s).
2. Install dependencies `pip install -r requirements.txt`.
3. Edit `acostsp['path']` in `config.py` to locate the acotsp executable.
4. Run using `python3`. Example usage: `python3 run.py -b -t ".ftv33.atsp" -i 100 -c 10 -n 1`.

## Tuning parameters
| Parameter     | Description   |
| ------------- |:-------------:|
| α      | The relative importance of the trail          |
| β      | The relative importance of the visibility     |
| ρ      | Trail persistence                             |
| Q      | A constant related to the quantity of trail laid by ants as trail evaporation |

(M. Dorigo et al. 1996)

## Tuning procedure

The tuning is performed using either random or Bayesian search (`-b | -r`) on
one TSPLIB instance at a time (`-tsp`). Tuning consists of calling the
Ant Colony Optimization algorithm *c* (`-c`) times with fixed number of
iterations *i* (`-i`), letting the tuning algorithm decide which parameters to evaluate for each of the *c* calls. This procedure is then repeated *n* (`-n`)
times. The results are recorded in a JSON file in the `/results` subfolder that
corresponds to the tuning algorithm used.
