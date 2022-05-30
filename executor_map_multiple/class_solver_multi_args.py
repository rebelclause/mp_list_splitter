import asyncio
from asyncio.queues import QueueFull, QueueEmpty
import concurrent.futures # ThreadPoolExecutor, ProcessPoolExecutor
import functools # partial
from quadratic_solver import Solver # typing the Queue item
from quadratic_solver import solver # obtaining the solver instance; Solver uses the special dunder method__call__(), so when arguments are received the calculation is run and result immediately returned
import numpy as np
import pickle
import math
from itertools import count
from dataclasses import dataclass, field
from typing import Any


# EXECUTOR = concurrent.futures.ThreadPoolExecutor
EXECUTOR = concurrent.futures.ProcessPoolExecutor
QUEUE_SIZE = 3
NUM_PROCESSES = 3
DELAY = 0.3
RUNCOUNT = count(1)


# TODO: nake a show out of 
# If the data elements are not comparable, the data can be wrapped in a class that ignores the data item and only compares the priority number:
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


async def print_queue(Q: asyncio.Queue):
    print("print queue")
    await asyncio.sleep(0)

    try:
        print(f"Outer Try 3: {Q.qsize()}")
        while True:
            print(f"Outer While 2: {Q.qsize()}")
            try:
                print(f"Try 2: {Q.qsize()}")
                while True:
                    # print(f"While 1: {Q.qsize()}")
                    # if Q.qsize() == Q.maxsize - 1:
                    #     await Q.join()
                    try:
                        # print(f"Try 1: {Q.qsize()}")
                        # item = await Q.get(block=False, timeout=30)
                        item:Solver = await Q.get()
                        # item = Q.get_nowait()
                        print(f"{next(RUNCOUNT)} - {item}")
                        if item != None:
                            ## the producer emits None to indicate that it is done
                            Q.task_done()
                            await asyncio.sleep(DELAY)
                        else:
                            # print(f"End: {Q.qsize()}")
                            print("Calculations ended...")
                            break
                    except Exception as e:
                        print(e)
                        continue
            except QueueFull as e:
                print(e)
                # Q.join()
                continue
            except Exception as e:
                print(e)

    except KeyboardInterrupt as e:
        exit()
    except Exception as e:
        print(e)
    finally:
        if Q.qsize() == Q.maxsize:
            print(f"Finally If True: {Q.qsize()}")
        else:
            print(f"Finally Else: {Q.qsize()}")
            print(f"{Q.maxsize=}")
            print('QQQQQQQQQ')


def solve(input):
    print(input)
    solver = Solver()
    result = solver(input)
    return result

def solve2(input):
    # print(input)
    a, b, c = input
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

def solve3(input):
    # print(input)
    return input

async def quadratic(Q: asyncio.Queue):
    """Example usage of functools.partial to call different functions with multiple arguments through a single point of intersect with a multiprocessing executor of the concurrent.futures standard library module."""
    print("quadratic")
    await asyncio.sleep(0)

    # inputs = np.random.rand(200,3)*100
    # # print(inputs)

    inputs = np.random.randint(1000000,size=(20,3))
    # for input in inputs:
    #     print(type(input))
    #     print(tuple(input))
    #     print(list(input))

    # # not needed, no immediately apparent issues with np.array
    # inputs = [tuple(x) for x in inputs]
    # print(inputs)

    # iter = [(4, 88, 342), (4, 88, 342), (4, 88, 342)]
    # lambda x: task(X*), iter

    task_results = []

    # from functools import partial
    # s = partial(solver, Q)
    # solver_map = map(lambda i: solve2(*i), inputs)
    # s_solver = pickle.dumps(solver_map)
    # print(s_solver)

    with EXECUTOR(NUM_PROCESSES) as executor:
        for task_result in executor.map(solver, inputs):
        # for task_result in executor.map(s, inputs): # no, the class outfitted with a passed Queue will not pickle... at least not the way it was done, using the partial
            await Q.put(task_result)
        # The Q might be full when given a maxsize, which one iteration of this mishmash does 
            # Q.put_nowait(task_result)
        # for task_result in executor.map(lambda i: solver(*i), inputs):
        # for task_result in executor.map(solve2, inputs):
        # for task_result in executor.map(solve3, inputs):
            # print(task_result)
            # task_results.append(task_result)
    # print("Cumulative and final: ", task_results)
    # print("Calculations ended...producer's end")
    # await Q.join()
    # return 'multiprocessing complete'

async def main():
    Q = asyncio.Queue(QUEUE_SIZE)
    tasks = await asyncio.gather(*[quadratic(Q), print_queue(Q)])
    print(tasks)

if __name__ == "__main__":
    # task = Solver()
    # print(task(8.8, 9.9, 11.9889))
    # print(task(3.0, 6.0, 257.0))
    # print(task(4, 88, 342))


    asyncio.run(main())

