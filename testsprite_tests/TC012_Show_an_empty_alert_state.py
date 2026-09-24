import asyncio
import re
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",
                "--disable-dev-shm-usage",
                "--ipc=host",
                "--single-process"
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        # Wider default timeout to match the agent's DOM-stability budget;
        # auto-waiting Playwright APIs (expect, locator.wait_for) inherit this.
        context.set_default_timeout(15000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> navigate
        await page.goto("http://localhost:5173/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Click the 'Early Warning Alerts' link in the left navigation to open the Alerts page.
        # Early Warning Alerts Urgent link
        elem = page.get_by_role('link', name='Early Warning Alerts Urgent', exact=True)
        await elem.click(timeout=10000)
        
        # -> Click the 'Watchlist' severity button to filter alerts to Watchlist and trigger the empty-state view.
        # Watchlist button
        elem = page.get_by_role('button', name='Watchlist', exact=True)
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Empty-state heading 'No Active Escalation Alerts' is visible in the Alerts page.
        # Assert-outcome: passed
        # Assert: The page displays the empty-state heading 'No Active Escalation Alerts'.
        await expect(page.locator("xpath=/html/body/div[1]/div/div/main/div/div/div[3]/div[1]/svg").nth(0)).to_contain_text("No Active Escalation Alerts", timeout=15000), "The page displays the empty-state heading 'No Active Escalation Alerts'."
        
        # --> An informational summary explaining there are no alerts for the selected filters is shown.
        await page.locator("xpath=/html/body/div[1]/div/div/main/div/div/div[3]/div[2]/button").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The 'Reset Severity & Status Filters' button is visible as a recovery action for the empty state.
        await expect(page.locator("xpath=/html/body/div[1]/div/div/main/div/div/div[3]/div[2]/button").nth(0)).to_be_visible(timeout=15000), "The 'Reset Severity & Status Filters' button is visible as a recovery action for the empty state."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    