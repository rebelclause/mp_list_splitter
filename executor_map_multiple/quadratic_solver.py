# courtesy of Jetbrains, an example on a page demonstrating the use of docker-compse container-based interpreters, for running and debugging, using different versions of Python than might be native on a development system



import math
from dataclasses import dataclass

class Solver:

    def __init__(self):
        ...
        # , a:float, b:float, c:float):
        # self.a = a
        # self.b = b
        # self.c = c

    def __call__(self, a: float, b: float, c: float):
        d = b ** 2 - 4 * a * c
        if d > 0:
            disc = math.sqrt(d)
            root1 = (-b + disc) / (2 * a)
            root2 = (-b - disc) / (2 * a)
            return root1, root2
        elif d == 0:
            return -b / (2 * a)
        else:
            return "This equation has no roots"

class SolverB:

    def demo(self, a, b, c):
        d = b ** 2 - 4 * a * c
        if d > 0:
            disc = math.sqrt(d)
            root1 = (-b + disc) / (2 * a)
            root2 = (-b - disc) / (2 * a)
            return root1, root2
        elif d == 0:
            return -b / (2 * a)
        else:
            return "This equation has no roots"


if __name__ == '__main__':
    solver = SolverB()

    while True:
        a = int(input("a: "))
        b = int(input("b: "))
        c = int(input("c: "))
        result = solver.demo(a, b, c)
        print(result)