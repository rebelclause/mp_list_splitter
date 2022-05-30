# courtesy of Jetbrains, an example on a page demonstrating the use of docker-compse container-based interpreters, for running and debugging, using different versions of Python than might be native on a development system


import math
from dataclasses import dataclass
import numpy
import asyncio

class Solver:

    def __call__(self, args):
        a, b, c, = args
        d = b ** 2 - 4 * a * c

        if d > 0:

            disc = math.sqrt(d)
            root1 = (-b + disc) / (2 * a)
            root2 = (-b - disc) / (2 * a)
            return f"{root1=}, {root2=} solves {a=}, {b=}, {c=}"

        elif d == 0:
            return f"As the discriminant is 0; {a=}, {b=}, {c=} gives {-b / (2 * a)}"
            # return -b / (2 * a)

        else:
            return f"No roots with {a=}, {b=}, {c=}"


solver = Solver()

if __name__ == '__main__':
    solver = Solver()

    while True:
        a = int(input("a: "))
        b = int(input("b: "))
        c = int(input("c: "))
        args = a, b, c
        result = solver(args)
        print(result)