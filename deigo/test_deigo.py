import os
import argparse
from numpy.random import RandomState
import math

low = 1e10
high = 1e11
size = int(1e5)

def is_prime(n):
    """Returns True if n is prime and False otherwise"""
    if not isinstance(n, int):
        raise TypeError("argument passed to is_prime is not of 'int' type")
    if n < 2:
        return False
    if n == 2:
        return True
    max = int(math.ceil(math.sqrt(n)))
    i = 2
    while i <= max:
        if n % i == 0:
            return False
        i += 1
    return True

def num_primes(seed, current_core_idx, total_cores):
    """Calculates number of primes in i-th portion of the array where i is the index of current core"""
    rs = RandomState(seed)
    rnd_array = rs.randint(low=low, high=high, size=size).tolist()
    numbers_per_core = math.ceil(len(rnd_array)/total_cores)
    start = current_core_idx * numbers_per_core
    stop = min(start + numbers_per_core, len(rnd_array))
    return sum(
        [
            1 
            for x in range(start, stop) 
            if is_prime(rnd_array[x])
        ]
    )


if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, required=True, help='Random seed')
    parser.add_argument('--cores', type=int, help='Number of cores')
    parser.add_argument('--dir', type=str, help='Output directory')
    args = parser.parse_args()

    if args.cores is None:
        args.cores = len(os.sched_getaffinity(0))

    output_file = None
    if args.dir:    
        if not os.path.exists(args.dir):
            os.makedirs(args.dir)
        seed_pad = str(args.seed).zfill(3)
        output_file = os.path.join(args.dir, f'output_{seed_pad}.txt')

    def log_info(s):
        print(s)
        if args.dir:
            with open(output_file, 'a') as fout:
                fout.write(s + '\n')

    log_info(f'Seed: {args.seed}')
    log_info(f'Num cores: {args.cores}')

    if args.cores == 1:
        total_primes = num_primes(args.seed, 0, 1)
    else:
        from joblib import Parallel, delayed
        runs_results = Parallel(n_jobs=args.cores)(
            delayed(num_primes)(args.seed, i, args.cores) \
            for i in range(args.cores)
        )
        # from multiprocessing import Pool
        # with Pool() as pool:
        #     runs_results = pool.starmap(
        #         num_primes, 
        #         [(args.seed, i, args.cores) for i in range(args.cores)]
        #     )

        total_primes = sum(runs_results)

    log_info(f'Total num of primes: {total_primes}')