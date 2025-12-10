'''Read digits from control file'''

import os
from pathlib import Path


CONTROL_FILE = Path(os.path.join(os.path.dirname(__file__), '..', '..', 'etc', 'pi-billion.txt')).resolve()


def pi_digits_from_file(nbytes: int, file: os.PathLike = CONTROL_FILE) -> str:
    data = ''

    with open(file, 'r', encoding='ascii') as f:
        data = f.read(nbytes)

    return '3' + data[2:]


def pi_digits(n: int) -> str:
    '''Copy n digits of pi from the control file'''
    nbytes = n + 1  # exclude '.', but include '3'
    return pi_digits_from_file(nbytes)


if __name__ == "__main__":
    import time

    print(f'{CONTROL_FILE=}')

    start = time.perf_counter_ns()

    n = 10  # _000_000  # number of digits
    pi_str = pi_digits(n)

    end = time.perf_counter_ns()

    # print(pi_str)

    elapsed = (end - start) / 1024 ** 2
    print(f'{n:_} digits in {elapsed:.03f} ms')
