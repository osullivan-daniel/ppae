#!/bin/bash
rm -rf .allure-results
python3 -m pytest --alluredir .allure-results/
allure serve .allure-results