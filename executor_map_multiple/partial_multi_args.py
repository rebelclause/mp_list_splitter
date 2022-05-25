import asyncio
import concurrent.futures # ThreadPoolExecutor, ProcessPoolExecutor
import functools # partial


EXECUTOR = concurrent.futures.ThreadPoolExecutor
NUM_PROCESSES = None


def api_call_one(*args, **kwargs):
    print(args)
    print(kwargs)

def api_call_two(*args, **kwargs):
    print(args)
    print(kwargs)

def api_call_three(*args, **kwargs):
    print(args)
    print(kwargs)

def hello(a, b):
    return f"{a.upper()} {b.upper()}"

async def main():
    """Example usage of functools.partial to call different functions with multiple arguments through a single point of intersect with a multiprocessing executor of the concurrent.futures standard library module."""

    payload = {}
    payload = {
        "somekey": "somestring",
        "option1": "option1string",
        "option2": "option2string"
    }

    command = 'get_request_one'

# prototype is an indicator stack, each with its own callable, but the symbol aggregation is simply for convenience of the example

# prototype is an ohlc update of symbols

# prototype is an ohlc init of symbols and the creation of symbol tables and associated base stack tables and indicator backtesting data

    iter_args = [
        [api_call_one, 'FEB/DBC', payload, command],
        [api_call_two, 'FEB/DBC', payload, command],
        [api_call_three, 'FEB/DBC', payload, command],
        [api_call_one, 'FEB/DBC', payload, command]]

    iter_partial_args = []
    iter_extracted = []
    for arg in iter_args:
        iter_partial_args.append(functools.partial(arg[0], arg[2], arg[3]))
        iter_extracted.append(arg[1])

    task_results = []
    NUM_PROCESSES = len(iter_args)
    with EXECUTOR(NUM_PROCESSES) as executor:
        for idx, _ in enumerate(iter_partial_args):
        print(f"Batch {idx + 1} of {len(iter_partial_args)} consisting of: {_}")
            for task_result in executor.map(_, iter_extracted):
                task_results.append(task_result)
            print("Cumulative and final: ", task_results)


if __name__ == "__main__":
    asyncio.run(main())

