import asyncio
import signal
from contextlib import aclosing
from pathlib import Path
from typing import AsyncGenerator

WATCH_DIR = Path("./tmp")
CONCURRENCY = 3
POLL_INTERVAL = 5
TASK_TIMEOUT = 10
SHUTDOWN_TIMEOUT = 15


# ----------------------------
# 非同期ジェネレータ
# ----------------------------
async def file_batch_generator(stop_event: asyncio.Event) -> AsyncGenerator[Path, None]:
    print("generator: started")
    try:
        while not stop_event.is_set():
            for file in WATCH_DIR.glob("*"):
                if file.is_file():
                    yield file
            await asyncio.sleep(POLL_INTERVAL)
    finally:
        print("generator: cleanup")


# ----------------------------
# ファイル処理
# ----------------------------
async def process_file(file: Path):
    print(f"processing: {file}")
    await asyncio.sleep(5)
    print(f"done: {file}")
    file.unlink(missing_ok=True)


# ----------------------------
# Runner
# ----------------------------
async def runner():
    WATCH_DIR.mkdir(exist_ok=True)

    stop_event = asyncio.Event()
    semaphore = asyncio.Semaphore(CONCURRENCY)
    loop = asyncio.get_running_loop()

    def shutdown_signal():
        print("shutdown signal received")
        stop_event.set()

    loop.add_signal_handler(signal.SIGINT, shutdown_signal)
    loop.add_signal_handler(signal.SIGTERM, shutdown_signal)

    async def worker(file: Path):
        async with semaphore:
            try:
                await asyncio.wait_for(
                    process_file(file),
                    timeout=TASK_TIMEOUT
                )
            except asyncio.TimeoutError:
                print(f"timeout: {file}")
            except asyncio.CancelledError:
                print(f"cancelled: {file}")
                raise
            except Exception as e:
                print(f"error processing {file}: {e}")

    try:
        async with asyncio.TaskGroup() as tg:
            async with aclosing(file_batch_generator(stop_event)) as gen:
                async for file in gen:
                    if stop_event.is_set():
                        break
                    tg.create_task(worker(file))

    except* Exception as eg:
        print(f"TaskGroup exception: {eg}")

    # ----------------------------
    # Shutdown制御（時間制限付き）
    # ----------------------------
    if stop_event.is_set():
        print("shutdown phase: waiting remaining tasks...")

        try:
            await asyncio.wait_for(
                asyncio.sleep(0),  # TaskGroupはここで既にjoin済
                timeout=SHUTDOWN_TIMEOUT
            )
        except asyncio.TimeoutError:
            print("shutdown timeout reached")

    print("runner stopped cleanly")


# ----------------------------
# エントリーポイント
# ----------------------------
if __name__ == "__main__":
    asyncio.run(runner())
