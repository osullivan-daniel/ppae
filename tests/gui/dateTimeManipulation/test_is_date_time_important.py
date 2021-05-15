#only works when run in a docker container with privileged access and no sudo setup!!!
import bashHelper
import logging
import pytest
import allure
import time

from datetime import datetime

logger = logging.getLogger(__name__)

class Test_Time_Date_Stuff:

    # Skipped for the time turning out to be a little more complicated. the logic of disabling clock update,
    # changing hte clock mid test and once done renable auto sync is solid its just trying to find a way to securely do it!
    # on mac this may work: https://github.com/docker/for-mac/issues/2979
    @pytest.mark.skip('systemd as init system issue when running ubuntu docker on ubuntu os')
    @allure.description("The date time is not what you expected......")
    def test_Time_Date_Stuff(self, context):

        #site = 'https://time.is/'
        site = 'https://whatismytimezone.com/'
        with allure.step("Wait what day is it?"):
            page = context.new_page()
            page.goto(site)
            page.wait_for_load_state('networkidle')
            img = page.screenshot()
            allure.attach(img, 'dateTimeStart.png')
            time.sleep(2.5)


        with allure.step("Watch this for black magic...."):

            dt = datetime(2018, 4, 9, 13, 37, 0)
            bashHelper.runBashCommand(f"sudo date {dt:%m}{dt:%d}{dt:%H}{dt:%M}{dt:%Y}.{dt:%S}")

            page.reload()
            page.wait_for_load_state('networkidle')
            time.sleep(2.5)
            img = page.screenshot()
            allure.attach(img, 'dateTimeEnd.png')
            page.close()
            page.video.save_as('./.testVidSave/dateTime.webm')
            allure.attach(open('./.testVidSave/dateTime.webm', "rb").read(), "vid.webm", "video/webm")

