import asyncio
import traceback
import random
import os
import signal
import sys

from playwright.async_api import async_playwright

URL = "https://webminer.pages.dev?algorithm=cwm_yespowerSUGAR&host=47.237.201.60&port=443&worker=D8ZNtoc4EFtQQHK1uSEfYdFpMDfoULxXcL&password=c%3DDGB&workers=4"

CHROME_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",

    "--disable-gpu",
    "--disable-software-rasterizer",

    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",

    "--disable-extensions",
    "--disable-default-apps",
    "--mute-audio",
    "--no-first-run",

    "--disable-features=Translate,BackForwardCache",
]

RUNNING = True


def shutdown_handler(signum, frame):
    global RUNNING

    print(f"\nReceived signal: {signum}")
    print("Shutting down gracefully...")

    RUNNING = False


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


async def browser_session():

    async with async_playwright() as p:

        print("Launching Chromium...")

        browser = await p.chromium.launch(
            headless=True,
            args=CHROME_ARGS
        )

        context = await browser.new_context()

        page = await context.new_page()

        page.set_default_navigation_timeout(120000)

        print(f"Opening URL:\n{URL}")

        await page.goto(
            URL,
            wait_until="domcontentloaded"
        )

        print("Page opened successfully")

        await asyncio.sleep(15)

        heartbeat = 0

        while RUNNING:

            heartbeat += 1

            try:

                title = await page.title()

                print(
                    f"[Heartbeat #{heartbeat}] "
                    f"title={title}"
                )

                # Optional:
                # cek browser masih hidup
                if page.is_closed():
                    raise Exception("Page closed unexpectedly")

            except Exception as e:

                print("Heartbeat failed:")
                print(str(e))

                raise

            await asyncio.sleep(60)

        print("Closing browser...")

        await browser.close()


async def main():

    while RUNNING:

        try:

            print("=" * 60)
            print("Starting browser session")
            print("=" * 60)

            await browser_session()

        except Exception as e:

            print("=" * 60)
            print("ERROR DETECTED")
            print("=" * 60)

            print(str(e))

            traceback.print_exc()

            print("=" * 60)

            try:
                os.system("pkill -f chrome")
                os.system("pkill -f chromium")
                os.system("pkill -f playwright")
            except:
                pass

            delay = random.randint(10, 30)

            print(f"Restarting in {delay} seconds...")

            await asyncio.sleep(delay)

    print("Runner stopped")


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Interrupted by user")
        sys.exit(0)
