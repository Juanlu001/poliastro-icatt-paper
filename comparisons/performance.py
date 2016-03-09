import time

import numpy as np

import astropy.units as u

from poliastro.bodies import Earth
from poliastro.iod import vallado, izzo

R_BASE = 1e6
V_BASE = 1e1
TOF_BASE = 86400.0

N_CASES = 1000000


def main():
    k = 3.986004362330e5

    t_start = time.process_time()
    for ii in range(N_CASES):
        r0 = np.random.uniform(-R_BASE, R_BASE, 3)
        r = np.random.uniform(-R_BASE, R_BASE, 3)
        tof = np.random.uniform(1000.0, TOF_BASE)

        solutions = [sol for sol in izzo._lambert(k, r0, r, tof, 0, 35, 1e-8)]

    t_end = time.process_time()

    return t_end - t_start, N_CASES / (t_end - t_start)


if __name__ == '__main__':
    print(main())