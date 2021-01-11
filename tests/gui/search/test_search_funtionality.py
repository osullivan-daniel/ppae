import time
import pytest
import allure
import logging

from bs4 import BeautifulSoup as bs4

logger = logging.getLogger(__name__)

class PropertyPalHelpers:

    @allure.step('Setup fake geolocation')
    def geolocationSetup(self, context, geoDict):
        logger.debug('geolocationSetup')
        context.setGeolocation(geoDict)
        context.grantPermissions(['geolocation'])
        return context.newPage()

    @allure.step('Navigate to home page')
    def navigateToHomePage(self, page, guiConfig):
        logger.debug('navigateToHomePage')
        page.goto(guiConfig['website'])
        page.waitForLoadState('networkidle')
        img = page.screenshot()
        allure.attach(img, 'homepage.png')

    @allure.step('Allow Cookies')
    def allowCookies(self, page):
        logger.debug('allowCookies')
        img = page.screenshot()
        allure.attach(img, 'wouldILikeCookies.png')
        page.waitForLoadState('networkidle')
        page.click('text=AGREE')
        img = page.screenshot()
        allure.attach(img, 'acceptedCookies.png')

    # example of additonal loging lines being added to allure
    @allure.step("Search for 'My Location'")
    def preformMyLocationSearch(self, page):
        logger.debug('preformMyLocationSearch')

        logger.debug('open drop down')
        page.click('div[class="search-ctrl query  suggestions-container"]')

        logger.debug('select text')
        page.click('text=My Location')

        logger.debug('take screen shot confirming selection')
        img = page.screenshot()
        allure.attach(img, 'selectMyLocation.png')

        logger.debug('select search to buy')
        page.click('button[class="btn btn-red btn-buy"]')

    @allure.step("Search by text")
    def preformTextSearch(self, page, searchText):
        logger.debug('preformTextSearch')
        page.click('div[class="search-ctrl query  suggestions-container"]')
        page.type('input[id=query]', searchText)
        img = page.screenshot()
        allure.attach(img, 'searchText.png')
        page.click('button[class="btn btn-red btn-buy"]')

    @allure.step("Assert No Results")
    def assertNoResults(self, page):
        logger.debug('assertNoResults')
        page.waitForSelector('.noresults-heading')
        img = page.screenshot()
        allure.attach(img, 'noResults.png')
        assert page.innerText('.noresults-heading') == 'SORRY, NO PROPERTIES FOUND'

    # you could possibly split this method in two one for my location and one for text, but you end up with duplication...
    @allure.step("Assert Results")
    def assertResults(self, page, searchType, searchString):
        logger.debug('assertResults')
        img = page.screenshot()
        allure.attach(img, f'resultsFor{searchString}.png')

        # Idealy anything your interacting with in automations tests will have an tag
        # as xpaths and selectors are always subject ot change
        if searchType == 'location':
            assert page.innerText('div.maxwidth > h1:nth-child(1)') == f'PROPERTY FOR SALE NEAR MY LOCATION'
        elif searchType == 'text':
            assert page.innerText('div.maxwidth > h1:nth-child(1)') == f'PROPERTY FOR SALE IN {searchString}'

        numOfPagesRes = page.innerText('.pgheader-currentpage')
        numOfResults = page.innerText('.pgheader-currentpage > em:nth-child(1)')

        numOfPages = int((numOfPagesRes.split('(')[0].split(' of ')[-1]).strip())
        curPageNum = int((numOfPagesRes.split('(')[0].split(' of ')[0].split('Page ')[-1]).strip())

        addressList = []
        while curPageNum <= numOfPages:

            handle = page.querySelector('.sr-widecol > ul:nth-child(1)')
            addressList, curPageNum = self.processPage(handle, addressList, page)

            if curPageNum != numOfPages:
                elemsnetHandle = page.querySelector('.paging-next')
                elemsnetHandle.scrollIntoViewIfNeeded()
                img = page.screenshot()
                allure.attach(img, f'nextButtonPage{curPageNum}.png')
                page.click('.paging-next')
            else:
                break

        assert int(numOfResults) == len(set(addressList))

        postCodeList = []
        for eachAddress in set(addressList):
            postCodesBs4 = eachAddress.find('span', class_='text-ib')
            postCodeList.append(postCodesBs4.text)

        postcodesFound = set(postCodeList)

        if searchType == 'location':
            # Without knowing exact parameters around a 'my location search' (i suspect its a distance based thing)
            # its hard to define a better test than ensuring at least one house for sale in our post code was returned
            # as several post codes can be returned
            assert searchString in postcodesFound


        elif searchType == 'text':
            assert len(postcodesFound) == 1
            assert postCodeList[0] == searchString



    def processPage(self, handle, addressList, page):
        logger.debug(f'processPage')
        numOfPagesRes = page.innerText('.pgheader-currentpage')
        curPageNum = int((numOfPagesRes.split('(')[0].split(' of ')[0].split('Page ')[-1]).strip())
        logger.debug(f'processing page number {curPageNum}')

        soup = bs4(handle.innerHTML(), 'html.parser')
        addressList.extend(soup.find_all('div', class_="propbox-details"))

        img = page.screenshot()
        allure.attach(img, f'topOfPage{curPageNum}.png')

        return addressList, curPageNum


class TestBT14PropertiesAvailable:

    @allure.description("test search 'my loaction' BT14")
    def testBT14PropertiesAvailable(self, guiConfig, context):
        pp = PropertyPalHelpers()
        geoDict = guiConfig['bt14']
        page = pp.geolocationSetup(context, geoDict)
        pp.navigateToHomePage(page, guiConfig)
        pp.allowCookies(page)
        pp.preformMyLocationSearch(page)
        pp.assertResults(page, 'location', 'BT14')


class TestBT6PropertiesAvailable:

    # At the time of writting this i noticed a bug in this the number of results says 104 but
    # there are infact 106 results (10 per page with 6 on the last)
    @allure.description("test search BT6")
    @pytest.mark.skip_browser("webkit")
    def testBT6PropertiesAvailable(self, guiConfig, context):
        pp = PropertyPalHelpers()
        page = context.newPage()
        pp.navigateToHomePage(page, guiConfig)
        pp.allowCookies(page)
        pp.preformTextSearch(page, 'BT6')
        pp.assertResults(page, 'text', 'BT6')


class TestNoPropertiesAvailable:

    @allure.description("test search 'my loaction' no results")
    def testNoPropertiesAvailable(self, guiConfig, context):
        pp = PropertyPalHelpers()
        # northAtlanticOcean coridantes should always return no results
        geoDict = guiConfig['northAtlanticOcean']
        page = pp.geolocationSetup(context, geoDict)
        pp.navigateToHomePage(page, guiConfig)
        pp.allowCookies(page)
        pp.preformMyLocationSearch(page)
        pp.assertNoResults(page)
