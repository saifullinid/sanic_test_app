import asyncio


def queue_filling(queue, data):
    queue.put(data)


async def use_worker(queue):
    while True:
        data = await queue.get()
        # TODO foo(data)
        queue.task_done()


def tasks_filling(loop, queue):
    tasks = []
    for _ in range(5):
        tasks.append(loop.create_task(use_worker(queue)))
    return tasks


def loop_run(loop, tasks):
    loop.run_until_complete(asyncio.wait(tasks))


def launch_async(loop, queue):
    tasks = tasks_filling(loop, queue)
    loop_run(loop, tasks)
