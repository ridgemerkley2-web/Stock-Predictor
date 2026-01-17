from dataclasses import dataclass
from typing import Iterable, List, Tuple


@dataclass
class TimeSplit:
    train: slice
    val: slice
    holdout: slice


def time_split(total: int) -> TimeSplit:
    train_end = int(total * 0.7)
    val_end = int(total * 0.85)
    return TimeSplit(slice(0, train_end), slice(train_end, val_end), slice(val_end, total))


def walk_forward_splits(
    total: int,
    train_window: int,
    val_window: int,
    step: int,
    expanding: bool = True,
) -> Iterable[Tuple[slice, slice]]:
    start = 0
    while start + train_window + val_window <= total:
        train_start = 0 if expanding else start
        train_end = start + train_window
        val_end = train_end + val_window
        yield slice(train_start, train_end), slice(train_end, val_end)
        start += step


def no_lookahead(features: List[float]) -> List[float]:
    shifted = [None]
    shifted.extend(features[:-1])
    return shifted
