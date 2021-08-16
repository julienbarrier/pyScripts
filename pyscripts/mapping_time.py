"""
Mapping time:
    functions to calculate how long a sweep will be
"""

from typing import Optional
from warning import warn
from datetime import datetime, timedelta


def sweep_1d(
    start: float,
    stop: float,
    sweep_up_rate: Optional['float'] = 0,
    sweep_down_rate: Optional['float'] = 0,
    waiting: Optional['float'] = 0,
    time_per_point: Optional['float'] = 1,
    **kw
) -> tuple[float]:

    """
    calculate the time necessary to carry out a 1d sweep.

    Args:
        start: sweep start point
        stop: sweep stop point
        sweep_up_rate: optional, /min
        sweep_down_rate: optional, /min
        waiting: optional
        time_per_point: optional, s

    Returns:
        tuple(float):
            time per sweep (min), number of points, step size
    """

    echo = kw.pop('echo', True)

    if not sweep_up_rate and not sweep_down_rate:
        warn("no sweep rate given")

    sweep_range = abs(stop - start)
    sweep_rate = min(sweep_up_rate, sweep_down_rate)

    time_per_sweep = 0
    if sweep_up_rate:
        time_per_sweep += sweep_range/sweep_up_rate
    if sweep_down_rate:
        time_per_sweep += sweep_range/sweep_down_rate
    if waiting:
        time_per_sweep += waiting
    time_per_sweep *= 60

    num = int(sweep_range/(sweep_rate*time_per_point/60))
    step = sweep_range/num

    if echo:
        print('the sweep will take {}min {}s to complete. \n'
              'you will record {} points (step size = {}) \n'
              'expected end time: {}\n'.format(
                  str(time_per_sweep//60),
                  str(time_per_sweep % 60),
                  str(num),
                  str(step),
                  datetime.now() + timedelta(seconds=time_per_sweep)
              ))

    return time_per_sweep, num, step


def sweep_2d(
    start_fast: float,
    stop_fast: float,
    sweep_up_fast: float,
    sweep_down_fast: float,
    start_slow: float,
    stop_slow: float,
    step: float,
    waiting: Optional['float'] = 0,
    time_per_point: Optional['float'] = 1,
    **kw
) -> tuple(float):

    echo = kw.pop('echo', True)
    if echo:
        print("time per sweep:f\n"
              "-----------------------------------\n")

    time_fast_sweep = sweep_1d(start_fast, stop_fast, sweep_up_fast,
                               sweep_down_fast, waiting=waiting,
                               time_per_point=1, echo=echo)[0]
    slow_sweep_range = abs(stop_slow - start_slow)
    cycles = int(slow_sweep_range/step) + 1

    time_per_map = cycles*time_fast_sweep

    if echo:
        print("-----------------------------------\n"
              "you will record {} cycles.\n "
              "it will take {}h {}min {}s to complete. \n"
              "expected end time: {}\n".format(
                  str(cycles),
                  str(time_per_map//3600),
                  str((time_per_map % 3600)//60),
                  str((time_per_map % 3600) % 60),
                  datetime.now() + datetime(seconds=time_per_map)
              ))

    return(time_per_map, cycles)
