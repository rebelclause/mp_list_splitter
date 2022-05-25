import asyncio
from list_splitter import mp_producer as producer
from channels import queue_channels
import json

# well timed foobar
wtf = "queue".isidentifier()
print(wtf)
# SNOOZE_SYNC = get_snooze(timer_default('this_segment')) # or on producer signal, but that's outside the queue, TODO: think on producer push wakeup of consumer, but test as is with a dynamically tuned producer, not the one off of this example

SNOOZE_SYNC = 30 

async def consumer(Q: asyncio.Queue):
    print('consumer ', __file__)
    await asyncio.sleep(0)
    
    deliverable:list = []
    
    # TODO: double global reference (here, and below, in q_handler()) may be related to mypy being used during debugging
    global count
    count = 0

    async def q_handler(message: str):
        global count
        if message == "heartbeat":
            print("Pumping life into the queue...")
            if count == 0:
                await asyncio.sleep(0)
                count += 1
                return
            elif count > 0:
                await asyncio.sleep(SNOOZE_SYNC)
                return
        count = 0
        if isinstance(message, int):
            print(":: task value --> ", message)
        elif isinstance(message, str):
            print(": sub-process update > ", message)
            # print(__file__, message)
        return

    try:
        while True:
            await Q.put("heartbeat")
            try:
                while not Q.empty():
                    try:

                        task = Q.get_nowait()

                        await q_handler(task)

                        Q.task_done()

                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

async def long_running(Q: asyncio.Queue, wait: int):
    # TODO:"As an attempt to inject a message into the queue and have it bypass the current heartbeat mechanics, long_running() is a failure. Success, however, may come with either converting the present Queue into a PriorityQueue, which would require messages to include a priority, and/or other optional arguments accompanying the included task, or to WRAP Queue in a PriorityQueue, sening control messages to the same handling mechanics as the inner Queue. Since this hasn't been tried on my end, and the thing is in a working state, one or more ideas like those above will likely be pursued, but at a later date. Being what they are, technical debt and a rising backlog could otherwise put snarls and swiping claws into this wrangle. Perhaps it is relevant to observe, two or more while loops do not meet under one function. They nest, and while the outer loops vest at rest, the inner loop does the daemon's work until those outside its inner domain come to collect their winnings, starting the cycle at any stepwise regression, progressing inward again on the whims of each encountered circle's satiated or unsatiated condition.

    print("long running: ", __file__)
    await asyncio.sleep(0)
    while True:
        print("long_running")
        Q.put_nowait(f"long running result... waiting {wait}")
        await asyncio.sleep(wait)


async def main():

    Q = await queue_channels('multiprocess')

    # batched_results = await producer(Q, 8)
    # print(batched_results)

    # workers = [consumer(Q), producer(Q, 9), long_running(Q, 10)]
    workers = [consumer(Q), producer(Q, 9)]

    # send_receive = await asyncio.gather(*[consumer(Q), producer(Q, 9), long_running(Q, 10)])

    # send_receive = await asyncio.gather(*workers)
       
    send_receive =  [asyncio.create_task(worker, name=worker) for worker in workers]
    for task in send_receive:
        await task
    


if __name__ == '__main__':
    asyncio.run(main())

