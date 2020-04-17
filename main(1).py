#!/usr/bin/env python3

import asyncio
import pyppeteer


async def checkRecaptcha(page):
    recaptcha = await page.querySelector('section[class="main"]')
    text = await recaptcha.getProperty('innerHTML')
    text = text.toString().lower()
    if 'bot check' in text:
        await asyncio.sleep(60)
        raise Exception('Captcha system triggered')


async def createPage(browser):
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'
    )
    return page


async def login(browser):
    page = await createPage(browser)
    await page.goto('https://www.toughsociety.com/')
    await page.waitForSelector('#LoginUsername')
    await page.type('#LoginUsername', '6IX9INE')
    await page.type('#LoginPassword', 'Codeman')
    await page.click('input[value="Sign in"]')
    await page.waitFor(5000)
    return page


async def crimes(page):
    await page.goto(
        'https://www.toughsociety.com/rank/crimes',
    )
    await checkRecaptcha(page)
    await page.waitForSelector('#cExtortPolitician5')
    checkAll = await page.Jx('//a[contains(text(), "Check All")]')
    await checkAll[0].click()
    await page.click('input[value="Commit Crimes"]')
    print('Commit crimes')


async def GTA(page):
    await page.goto(
        'https://www.toughsociety.com/rank/gta',
    )
    await checkRecaptcha(page)
    await page.waitForSelector('span[class="push-slight-left"]')
    stealCar = await page.Jx('//button[contains(text(), "Steal Car")]')
    if len(stealCar) > 0:
        await stealCar[0].click()
        print('Stole car')


async def melt(page):
    await page.goto(
        'https://www.toughsociety.com/rank/melt/0',
    )
    await checkRecaptcha(page)
    await page.waitForSelector('table[class="mt-1 w-98"]')
    trList = await page.querySelectorAll('tr')
    try:
        for tr in trList[1:]:
            text = await tr.getProperty('innerHTML')
            text = text.toString().lower()
            if 'rare' not in text:
                button = await tr.querySelector('input')
                text = await button.getProperty('innerHTML')
                await button.click()
                print('Melting')
                break
        await page.click('input[type="submit"]')
    except Exception:
        pass


async def jail(page):
    await page.goto(
        'https://www.toughsociety.com/rank/jail',
    )
    await checkRecaptcha(page)
    await page.waitForSelector('input[type="submit"]')
    jailAll = await page.querySelectorAll('input[name="BustID"]')

    if len(jailAll) > 0:
        print('busted someone')
        await jailAll[0].click()
        await page.click('input[value="Bust out of Jail"]')


async def main():
    while True:
        browser = await pyppeteer.launch({
            'headless': True,
            'args': ['--no-sandbox']
        })
        try:
            page = await login(browser)
            while True:
                await page.waitFor(100)
                await crimes(page)
                await page.waitFor(100)
                await GTA(page)
                await page.waitFor(100)
                await melt(page)
                await page.waitFor(100)
                for i in range(10):
                    await page.waitFor(100)
                    print('jail')
                    await jail(page)
        except Exception as e:
            await browser.close()
            print('Error: {}'.format(e))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
