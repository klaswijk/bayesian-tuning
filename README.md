# bayesian-tuning
Bayesian parameter tuning of the Ant Colony Metaheuristic applied to the Travelling Salesman Problem

## How to use
1. Make sure you have both a [libaco](https://github.com/emmyyin/libaco) executable and one or more [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/) intance(s).
2. Install dependencies `pip install -r requirements.txt`.
3. Edit `acostsp['path']` in `config.py` to locate a .
4. Run using `python3`. Example usage: `python3 run.py -b -t ".ftv33.atsp" -i 100 -c 10 -n 1`.
