import time
import collections

import numpy as np

import astropy.units as u

from poliastro.bodies import Earth
from poliastro.jit import jit
from poliastro.iod import vallado, izzo

R_BASE = 1e6
V_BASE = 1e1
TOF_BASE = 86400.0

N_CASES = 1000000


@jit
def main():
    for ii in range(N_CASES):
        k = 3.986004362330e5
        r0 = np.zeros(3)
        r = np.zeros(3)
        for ii in range(3):
            r0[ii] = np.random.uniform(-R_BASE, R_BASE)
            r[ii] = np.random.uniform(-R_BASE, R_BASE)

        tof = np.random.uniform(1000.0, TOF_BASE)

        sol1, = izzo._lambert(k, r0, r, tof, 0, 35, 1e-8)

    return sol1


if __name__ == '__main__':
    t_start = time.process_time()
    print(main())
    t_end = time.process_time()
    print((t_end - t_start), N_CASES / (t_end - t_start))
