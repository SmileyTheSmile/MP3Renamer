import time


def test_function(function) -> float:
    start = time.perf_counter()
    function()
    end = time.perf_counter()

    return start - end
