import asyncio
import concurrent.futures

def hello(a, b):
    return f"{a.upper()} {b.upper()}"

async def main():
    iter_args = [
        ("firstname", "lastname"),
        ("namefirst", "namelast"),
        ("yourfirst", "yourlast"),

    ]

    task_results = []
    NUM_PROCESSES = len(iter_args)

    with concurrent.futures.ThreadPoolExecutor(NUM_PROCESSES) as executor:
        for task_result in executor.map(lambda i: hello(*i), iter_args):
            task_results.append(task_result)
        print(task_results)

if __name__ == "__main__":
    asyncio.run(main())



