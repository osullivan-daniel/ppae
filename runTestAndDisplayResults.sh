#!/bin/bash
rm -rf .allure-results
# Because dateTimeManipulation changes the clock we run it separately after the rest to avoid any interference (confirm test scoping may not be necessary)
python3 -m pytest -k 'not dateTimeManipulation' --alluredir .allure-results/
python3 -m pytest -k dateTimeManipulation --alluredir .allure-results/
allure serve .allure-results