import asyncio
from core.event_log import EventLog
import nodriver as uc


async def main(config: dict, eventLog: EventLog):
    browser = await uc.start(
        browser_executable_path=config["browserExecutablePath"],
        headless=True,
        browser_args=[
            "--window-size=1920,1080",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        ],
    )

    page = await browser.get(
        "https://accounts.google.com/AccountChooser/signinchooser?continue=https%3A%2F%2Fclassroom.google.com%2F&theme=mn&ddm=0&flowName=GlifWebSignIn"
    )
    await page
    try:
        email_field = await page.select("#identifierId", timeout=3)
        await email_field.send_keys(config["email"])
        next = await page.select("#identifierNext > div > button")
        await next.click()
        await page

        await page.wait_for("#password")

        password_field = await page.select(
            "#password > div:nth-child(1) > div > div:nth-child(1) > input"
        )
        await password_field.send_keys(config["password"])
        next = await page.select("#passwordNext > div > button")
        await next.click()
        await page

    except asyncio.TimeoutError:
        #print("Already logged in")
        pass

    while True:
        await asyncio.sleep(3)
        await page.get("https://classroom.google.com/u/0/a/not-turned-in/all")
        await page
        try:
            await page.wait_for(".I2pI", timeout=20)  # Wait for assignments to load
        except asyncio.TimeoutError:
            # Sometimes fails, not sure why
            pass
        assignments = await page.select_all(".I2pI")

        dropdowns = await page.select_all(".e2urcc")

        currentIdentifier = "This week"
        assignmentData = []

        for dropdown in [dropdowns[1], dropdowns[2]]:
            await dropdown.click()
            try:
                await dropdown.children[-1].children[0].click()
                # View all button at end of list ^^
            except:
                pass
            for li in dropdown.children:
                target = li
                for i in range(3):
                    target = target.children[0]

                target = target.children[1].children[0]  # Avoid image

                assignmentName = target.children[0].children[0].text
                assignmentDue = target.children[1].children[0].text
                assignmentData.append({"name": assignmentName, "due": assignmentDue})
            currentIdentifier = "Next Week"

        if len(assignmentData) > 0:
            eventLog.add({"type": "google_classroom", "data": assignmentData})

        await asyncio.sleep(60 * 10)  # 10 minutes
