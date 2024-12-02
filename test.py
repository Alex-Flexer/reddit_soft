from multiprocessing import Process
from time import sleep, time as now


def f(name):
    sleep(10)
    print('hello', name, now())


def d() -> list[Process]:
    names = ["bob", "alex", "felix", "daria", "boris", "maria"]
    process: list[Process] = []
    lf = lambda func, args: Process(target=func, args=args)

    for name in names:
        p = lf(f, (name,))
        p.start()
        process.append(p)

    return process


if __name__ == "__main__":
    d()
