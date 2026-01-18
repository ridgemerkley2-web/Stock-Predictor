from apps.worker.research import no_lookahead, time_split, walk_forward_splits


def test_no_lookahead_shift():
    features = [1, 2, 3]
    shifted = no_lookahead(features)
    assert shifted == [None, 1, 2]


def test_time_split():
    split = time_split(100)
    assert split.train == slice(0, 70)
    assert split.val == slice(70, 85)
    assert split.holdout == slice(85, 100)


def test_walk_forward_splits():
    splits = list(walk_forward_splits(total=100, train_window=60, val_window=10, step=10))
    assert splits[0] == (slice(0, 60), slice(60, 70))
    assert splits[1] == (slice(0, 70), slice(70, 80))
