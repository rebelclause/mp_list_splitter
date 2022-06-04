# Multiprocessing in Python, Examples

This repository is in no way exhaustive enough to cover all scenarios you might encounter. For that, your use case, particularly the data path and shape, will come in handy.

Two examples flesh out using `functools.partial` and `lambda:x` for mapping more than one argument to the function you want to run against a list of iterables, in a multi-process, or multi-threaded scenario.

Also, instead of static examples using synchronous code throughout, the Event loop is called into play such that asyncio.Queue task functions can be demonstrated.

The 'premium' example for this is `list splitter.py` which, in concert with `main.py` and the `channels.py` reveals the complete `asyncio.Queue` roundtrip of 'tasks' between a producer and a consumer. 

The list splitting is a secondary requirement-based result and, with a good understanding of the other examples, mostly unnecessary for using `executor.map()`. 

Several opportunities are hinted at for `list_splitter.py`, the one germane to most projects probably in the code near the tail end of the producer, employing recursive task renewal; it's here you could insert a consumer, linking another producer into the chain.

Whatever you do, don't get discouraged; sorting out a Task from a Future and the high level subtlety between them that links to the low level codebase can be challenging. Future examples may use a different form of Future (see what I did there) than the one shown here. You'll be chunking results with this code for now, but knowing it will help you identify other opportunities to optimize program flow and how Futures fit into that. 

When it doubt, the most synchronous-like method for running code in an async program is, easily, `asyncio.create_task(coro, name="")`. You'll see this several times. Please feel encouraged to tear into it and the use of `await asyncio.sleep(0)` at the top of tasks you want to run concurrently. Parallelism, aside, if you can do asycnio, your code may already be more optimized for speed than corresponding synchronous code.


## EXECUTORS of concurrent.futures

Both examples can be adapted to use either executor. Simply change the reference, and then run the code.

> concurrent.futures.ThreadPoolExecutor

> concurrent.futures.ProcessPoolExecutor


## Anticipating The Need For Massive Throughput And Processing Power

Running main.py, you may find, with small changes, the code can be a bit fussy, which, to my mind, suggests it needs some ironing out, possibly simplification, maybe more finesse on exceptions-based control flow. 

One of its clever features is the heartbeat in `main.py > consumer()`, but this may also be one of its worst problems, in that; flow is interrupted longer than delays set in the producer when the Queue is empty, meaning timely arrivals (as supposed to be eventually released to the Event Loop by an awaited `asyncio.sleep() / timer`) may not run as expected. One suggestion in comments may be to implement the primary Queue should be changed to a PriorityQueue. 

If you'd like to see that, give me a shout, and I can make an adaptation which shows this feature along with the consumer queue mentioned for at the tail end of the producer in `list_splitter.py`.

##### Resources:

[asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html?highlight=asyncio%20queue#asyncio.Queue)

[Launching Parallel Tasks: Executor Objects](https://docs.python.org/3/library/concurrent.futures.html?highlight=launching%20parallel%20tasks%20processpoolexecutor%20threadpoolexecutor#module-concurrent.futures)

[ProcessPoolExecutor.map() vs. ProcessPoolExecutor.submit()](https://superfastpython.com/processpoolexecutor-map-vs-submit/)

[Pass Multiple Parameters To: concurrent.futures.EXECUTOR.map](https://stackoverflow.com/questions/6785226/pass-multiple-parameters-to-concurrent-futures-executor-map)

[The Python pickle Module: How to Persist Objects in Python
](https://realpython.com/python-pickle-module/)


##### Disclaimer:

No warranty, mechantability, or libability on this one. Not guaranteed to work, and not guaranteed to prevent your computer and its software from blowing up. 

Frequent users of any favored IDE will know the pain of debugging Python's asynchronous code and all the fun (and not) that can be had with stack traces. 

FWIW, the 'premium' example ran for several days without an error, but as it is a 'closed loop' in the sense that its data and flow are contained and its shape well known. Consequently the data used serializes well and therefore didn't cause any major hair-pulling problems. 

This is an important fact that might best have been put in the introduction and aptly titled: Your Python Queue Loves A Pickle, But You Don't Want To Be In One If You Don't Take That In And Make Your Data Coding Behave Accordingly.



