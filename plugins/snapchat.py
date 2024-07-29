import asyncio
import nodriver as uc

from core.event_log import EventLog
from core.exceptions import BrowserError
from core.logger import Logger

log = Logger()


async def newSnaps(page: uc.Tab, browser: uc.Browser) -> dict:
    output = {}

    elems = await page.select_all(
        "div > span[id^=status] > span[class*=nonIntl]"
    )  # Selector for new snap message

    for elem in elems:
        await elem.flash()
        ancestor = elem
        for _ in range(5):  # 5 levels up
            ancestor = ancestor.parent
            target = ancestor.children[0].children[0]  # Messy way to grab name
        if "New Snap" in elem.text:
            output[elem.text] = f"snap from {target.text}"
        elif "New Chat" in elem.text:
            output[elem.text] = f"chat from {target.text}"
        elif "New" in elem.text and "Snap" not in elem.text and "Chat" not in elem.text:
            output[elem.text] = f"other from {target.text}"

    return output


async def otherFriends(page: uc.Tab, browser: uc.Browser) -> list:
    output = []

    elems = await page.select_all(
        "div > span[id^=status]  > span[class*=nonIntl]"
    )  # Selector for new snap message:
    # span with class nonIntl nested within a span with id beginning with status within a div

    for elem in elems:
        await elem.flash()
        ancestor = elem
        for _ in range(4):  # 4 levels up
            ancestor = ancestor.parent
            target = ancestor.children[0].children[0]

        output.append(elem.text + " - " + target.text)

    return output


async def main(config: dict, eventLog: EventLog):
    browser = await uc.start(
        # user_data_dir=config["dataDir"],
        browser_executable_path=config["browserExecutablePath"],
    )
    page = await browser.get("https://web.snapchat.com")
    html = await page.get_content()

    if "Browser not supported" in html:
        log.Error("Snapchat reports browser not supported")
        return
    await browser.wait(10)

    try:
        found = await page.find('//*[@id="ai_input"]', timeout=20)
        await asyncio.sleep(5)
        await found.click()
        await found.send_keys(config["username"])
        await asyncio.sleep(10)
        login_btn = await page.select(
            "#__next > main > div> div > div > div > form > div > span > button"
        )
        await asyncio.sleep(3)
        await login_btn.click()
        await browser.wait(7)
        try:
            await found.send_keys("\r\n")
            await browser.wait(7)
        except:
            pass

        try:
            cookie_btn = await page.find(
                '//*[@id="password-root"]/div/div[4]/div/section/div/div/div[3]/button[2]',
                timeout=2,
            )
            await cookie_btn.click()
        except:
            # Not a priority
            pass

        pwdfield = await page.find('//*[@id="password"]')
        await pwdfield.click()
        await pwdfield.send_keys(config["password"])

        login_btn = await page.find('//*[@id="password_form"]/div[3]/button')
        await login_btn.click()
        await browser.wait(5)

        # Notif popup
        nothanks = await page.find(
            '//*[@id="root"]/div[1]/div[2]/div/div/div[4]/div[2]/button[1]'
        )
        await nothanks.click()

    except Exception as e:
        raise e
        # We are already logged in
        pass

    while True:
        log.debug("Parsing content...")
        try:
            new = await newSnaps(page, browser)
        except:
            new = []
        # others = await otherFriends(page, browser)
        await asyncio.sleep(10)
        if len(new) > 0:
            existingSnaps = False
            for event in eventLog.events:
                if event["type"] == "snapchat":
                    existingSnaps = True
                    if event["data"] != new:
                        eventLog.add({"type": "snapchat", "data": new})
                    else:
                        pass
            if not existingSnaps:
                eventLog.add({"type": "snapchat", "data": new})
        else:
            eventLog.removeOfType("snapchat")

        await asyncio.sleep(5)

    await page.close()
