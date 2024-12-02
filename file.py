from threading import Thread
from multiprocessing import Process
from time import sleep


def bar():
    while True:
        sleep(0.5)
        print("working func \"bar\"")


def foo():
    thr = Thread(target=bar, daemon=True)
    thr.start()

    for i in range(4):
        print("working func \"foo\"", i)
        sleep(1)

    print("finish foo working!")


if __name__ == "__main__":
    thr = Process(target=foo)
    thr.start()
    thr.join()

    sleep(5)
