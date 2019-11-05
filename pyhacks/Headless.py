import asyncio
from pyppeteer import launch

class Headless:
    def __init__(self):
        # self.handle_function = handle_function
        # self.event_name = event_name # e.g. "request"
        self.browser = None
        loop = asyncio.new_event_loop()
        self.loop = loop
        asyncio.set_event_loop(loop)
        print("here")
        asyncio.ensure_future(self.init_browser())
        print("here2")

    async def init_browser(self):
        self.browser = await launch(args=["--no-sandbox"])

    async def runHeadless(self, url, event_name, handle_function):
        page = await self.browser.newPage()
        page.on(
            event_name,
            lambda request: asyncio.ensure_future(handle_function(request))
        )

        await page.goto(url)
        # test = await page.evaluate('() => return document.location')
        # print(test)
        # await page.screenshot({'path': 'example.png'})
        await page.close()

    async def close(self):
        await self.browser.close()
    
    def browse(self, url, event_name, handle_function):
        print("here3")
        self.loop.run_until_complete(self.runHeadless(url, event_name, handle_function))
        print("here4")
        # self.runHeadless()