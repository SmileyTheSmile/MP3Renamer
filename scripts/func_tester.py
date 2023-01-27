import time


def test_wrap(function, *args, **kwargs):
    start = time.perf_counter()
    result = function(*args, **kwargs)
    end = time.perf_counter()

    print(f"{end - start}")

    return result

def test(function, *args, **kwargs):
    start = time.perf_counter()
    function(*args, **kwargs)
    end = time.perf_counter()

    print(f"{end - start}")

