#!/bin/bash
rm -rf .allure-results
rm -rf .allure-reports
rm -rf allure-resultsC
rm -rf allure-resultsCF
rm -rf allure-resultsCFW

python3 -m pytest --alluredir .allure-results/
cp -rf .allure-results/ .allure-resultsC/
cp -rf .allure-reports/history/ .allure-results/
allure generate .allure-results -o .allure-reports --clean

rm -rf .allure-results
python3 -m pytest --alluredir .allure-results/ --browser firefox
cp -rf .allure-results/ .allure-resultsCF/
cp -rf .allure-reports/history/ .allure-results/
allure generate .allure-results -o .allure-reports --clean

rm -rf .allure-results
python3 -m pytest --alluredir .allure-results/ --browser firefox --browser webkit
cp -rf .allure-results/ .allure-resultsCFW/
cp -rf .allure-reports/history/ .allure-results/
allure generate .allure-results -o .allure-reports --clean

allure serve .allure-results/