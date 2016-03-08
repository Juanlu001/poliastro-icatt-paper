import pytest

import astropy.units as u

from poliastro.bodies import Earth
from poliastro.iod import vallado, izzo


def lambert_solution(lambert, *args, **kwargs):
    return next(lambert(*args, **kwargs))


def test_lambert_single_rev_vallado(benchmark):
    k_ = Earth.k.to(u.km ** 3 / u.s ** 2).value
    r0_ = ([15945.34, 0.0, 0.0] * u.km).value
    r_ = ([12214.83399, 10249.46731, 0.0] * u.km).value
    tof_ = (76.0 * u.min).to(u.s).value

    benchmark(vallado._lambert, k_, r0_, r_, tof_, True,
              numiter=35, rtol=1e-8)


def test_lambert_single_rev_izzo(benchmark):
    k_ = Earth.k.to(u.km ** 3 / u.s ** 2).value
    r0_ = ([22592.145603, -1599.915239, -19783.950506] * u.km).value
    r_ = ([1922.067697, 4054.157051, -8925.727465] * u.km).value
    tof_ = (10 * u.h).to(u.s).value

    benchmark(lambert_solution, izzo._lambert, k_, r0_, r_, tof_, 0,
              numiter=35, rtol=1e-8)


def test_lambert_multi_rev_izzo(benchmark):
    k_ = Earth.k.to(u.km ** 3 / u.s ** 2).value
    r0_ = ([22592.145603, -1599.915239, -19783.950506] * u.km).value
    r_ = ([1922.067697, 4054.157051, -8925.727465] * u.km).value
    tof_ = (10 * u.h).to(u.s).value

    benchmark(lambert_solution, izzo._lambert, k_, r0_, r_, tof_, 1,
              numiter=35, rtol=1e-8)
