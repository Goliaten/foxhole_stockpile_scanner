from source.Logger import Logger


def in_out_wrapper(fnc):

    def inner(*args, **kwargs):
        Logger().get().debug(f"Entering {fnc.__name__}")
        out = fnc(*args, **kwargs)
        Logger().get().debug(f"Exiting {fnc.__name__}")
        return out

    return inner
