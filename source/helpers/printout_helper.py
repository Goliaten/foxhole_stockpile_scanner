def in_out_wrapper(fnc):

    def inner(*args, **kwargs):
        print(f"Entering {fnc.__name__}")
        out = fnc(*args, **kwargs)
        print(f"Exiting {fnc.__name__}")
        return out

    return inner
