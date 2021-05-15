import allure
import logging
import bashHelper

logger = logging.getLogger(__name__)

class Test_Faux_Bdd_And_Video:

    @allure.description("Faux BDD example with video")
    def test_Faux_Bdd_And_Video(self, context):
        bashHelper.runBashCommand("date")

        site = 'adidas.co.uk'
        with allure.step("Given I go to google.com"):
            page = context.new_page()
            page.goto('https://google.com/')
            page.wait_for_load_state('networkidle')

        with allure.step("When I accept the cookies"):
            page.click('text=I agree')

        with allure.step(f"And I search for {site}"):
            page.type('[title="Search"]', site)
            page.keyboard.press('Enter')
            page.wait_for_selector(f"text=https://www.{site}")

        with allure.step(f"Then {site}  should be displayed in the results"):
            visible = page.is_visible(f"text=https://www.{site}")
            img = page.screenshot()
            allure.attach(img, 'results.png')
            assert visible
            page.close()
            page.video.save_as('./.testVidSave/fauxbdd.webm')

        allure.attach(open('./.testVidSave/fauxbdd.webm', "rb").read(), "vid.webm", "video/webm")



