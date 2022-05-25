import asyncio
import concurrent.futures
import random
from itertools import count as counter
import json



RATE_LIMIT = 3
CHUNK_SIZE = 25 # also num processpoolexecutor processes
NUM_PROCESSES = CHUNK_SIZE - 10
PRODUCER_COUNT = counter(1)
"""ProcessPoolExecutor as executor may experience a pickling error if the function running the task is not pickleable. Investigation is ongoing where hashing and the equality operator of passed Dataclass instances are concerned. Using json.dumps(), or pickle.dumps() may reveal some of the issues with data that wants to be passed, or one of these may be used to solve problems with inter-queue serialization altogether, with some Task class or other instantiated on the side where the task must be activated, from serialized data. Going this route also prepares data flow to be inclusive of other async task queues, and network transmission.

The example below has a number of alternate logical paths and console print statements seen in a number of commented lines. This file can be run without main, however, the best expression, and the one working best with present options is best launched from main().
"""

def execute_parallel(item_from_chunk: int):
    global Q
    # print(f"^^^^^^< -{item_from_chunk}- >_______")
    # taskname = asyncio.current_task()
    # print(f"{taskname = }")
    calculated = item_from_chunk**50
    # Q.put_nowait(calculated)
    return calculated

def list_splitter(data:list, chunk_size: int):
    # (item for chunk in result for item in chunk)
    n = chunk_size
    # print(f"{data = }")
    if n is None:
        n = 3
    _chunks = []
    chunklen = 0
    while len(data) != 0:
        chunk = data[0:n]
        _chunks.append(chunk)
        chunklen = len(chunk)
        while chunklen > 0:
            data.pop(0)
            chunklen -= 1
    if len(_chunks) == 1:
        # print(_chunks)
        return _chunks[0]
    else:
        # print(_chunks)
        return _chunks


# for item in mylist:
# 	result = task(item)
# results = map(task, mylist)

# for result in results:
# 	print(result)

# for result in map(task, mylist):
# 	print(result)

# for result in executor.map(task, mylist):
# 	print(result)

async def mp_producer(Q: asyncio.Queue, CHUNK_SIZE: int):
    print("mp_producer: ", __file__)
    await asyncio.sleep(0)

    # generate a randomly-sized list of random integers, both observing upper and lower bound limits
    long_list = [random.randint(1, 100) for i in range(random.randint(1, 100))]
    # chunk the list 
    _chunked_list = list_splitter(long_list, chunk_size=CHUNK_SIZE)

    try:
        print(f'outer_ring: task {asyncio.current_task().get_name()}')
        while True:
            try:
                # Alternately:
                    # tasks = [loop.create_task(execute_parallel(_chunked_list[i])) for i in range(len(_chunked_list))]
                    # loop.run_until_complete(asyncio.wait(task))
                
                tasks = _chunked_list
                final_result = []
                for idx, task in enumerate(tasks):
                    chunk_result = []
                    # process each item in the chunk of the _chunked_list
                    if not isinstance(task, list):
                        print(task)
                        task = list(task)
                    print(f"Batch {idx + 1} of {len(tasks)} consisting of: {task}")
                    NUM_PROCESSES = len(task)
                    with concurrent.futures.ProcessPoolExecutor(NUM_PROCESSES) as executor:
                        # TODO: retool with functools.partial to include Q as an argument to execute_parallel, bypassing Q.put here, if it's possible...

                        for task_pool_result in executor.map(execute_parallel, task):
                            # print(task_pool_result)
                            # print('', end='')
                            chunk_result.append(task_pool_result)
                            await Q.put(task_pool_result)
                    await Q.put(f"subtotal: {chunk_result}")
                        # print(chunk_result)
                        # print('', end='')
                    # print(Q.qsize())
                    final_result.extend(chunk_result)
                await Q.put(f"total: {final_result}")
                await asyncio.sleep(RATE_LIMIT)

            except Exception as e:
                print(e)
            except KeyboardInterrupt as e:
                exit()
            finally:
                while True:
                    await Q.join()
                    print(f"inner tail - finally")
                    
                # print(f"{final_result = }")
                # # TODO: following bootstrap init list from either source or state, subscription here to an input Queue???
                    workers = [mp_producer(Q, CHUNK_SIZE)]
                    repeat = [asyncio.create_task(worker, name=f'rerun_producer-{next(PRODUCER_COUNT)}') for worker in workers]
                    for task in repeat:
                        await task
                    await asyncio.sleep(5)

            # final_result.append(chunk_result)
            # import itertools # could also simply extend rather than append
            # final_result = list(itertools.chain.from_iterable(final_result))
            # await Q.put(final_result)
            
    except TypeError as e:
        print(f"TypeError -- {e}")
        exit()

    except Exception as e:
        await Q.join()
        print(f"outer tail: {e}")
        print(tasks)
        if e.search("object of type 'int' has no len()"):
            print("fatal error has ocurred, must reschedule the job list")
            exit()

    # finally:
    #     print('returning final result')
    #     return final_result

        # TODO: investigate queue.put() on as_completed()... concurrent.futures, vs asyncio.Future... confusion matrix stuff...
        # future = asyncio.current_task()
        # future.set_result(final_result)



if __name__ == '__main__':
    # obtain the event loop, or create one
    loop = asyncio.get_event_loop()

    # tidy example
    from concurrent.futures import ProcessPoolExecutor as Executor

    def fn(i):
        print(f'Hello')
        return 'World'

    with Executor(1) as executor:
        nums = [1, 2, 3]
        # future = executor.submit(fn(1))
        # print(future.result())
        for future in executor.map(fn, nums):
            print(future)
        # won't give TypeError: 'NoneType' if no param is passed to fn

    print("Too Many")

    # from typing import Generic, AsyncContextManager, TypeVar
    # # https://github.com/python/mypy/issues/9261

    # T_Item = TypeVar('T_Item', str, int)

    # class Foo(Generic[T_Item]):
    #     async def foo(self, manager: AsyncContextManager):
    #         async with manager:
    #             pass

    dummy_queue = asyncio.Queue()
    asyncio.run(mp_producer(dummy_queue, CHUNK_SIZE))

    # TODO: return futures, as_completed via the executor using run_in_executor()???
    # deliverable = []
    # for i in range(10):
    #     # asyncio.run_until_complete(main())
        
    #     concurrent.futures.as_completed
        
    #     result = asyncio.run_coroutine_threadsafe(main(loop), loop)
    #     deliverable.extend(future)
    # for package in deliverable:
    #     print(package)


