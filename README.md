# demo-automation

demo auto showing techniques


## Docker Image
uppae: Ubuntu, python, playwright, allure example

### Prerequisites
Install docker
depending on your installation you may need admin permissions for the following

### Build a new image
from the docker directory run:
docker build . -t uppae
NOTE - brew is very slow to set up so its worth kicking off the build and coming back after a while

### run your new image
docker run -it uppae

### Next steps
run the following commands (keygen creates silently with no passphrase)
eval $(~/.linuxbrew/bin/brew shellenv)
ssh-keygen -f ~/.ssh/id_rsa -q -P ""
Stick it in you preferred repo and away you go

## Ruinning From Local Machine

### Required Libraries 

Libraries required to be installed before use:

Please install python3 & pip3
Please install brew for mac or linux (allure has many dependancies and its the most robust way of installing it)

brew install allure  (brew update && brew upgrade - can be used to update installed packages)
 
pip3 install -U pytest  
pip3 install -U allure-pytest  
pip3 install -U pytest-playwright

### run and display results script

./runTestAndDisplayResults.sh -> will automatically run the tests and display the allure results


##Manual running info

### Base Command
The minimum required to run from the command line::

`python3 -m pytest`

### Optional Flags

-k '[module/testcase]' --> run specific module or test cases  
--env [config yml file path] --> config file - Current default is dev  
--alluredir [full path to where you wish to store the files]
-o log_cli=true --> terminal logging even if tests pass
--browser --> firefox webkit (chromium is set in pytest.ini so will always run) NOTE --browser is needed for each additonal browser
--headful --> runs the browser

### View allure reports
allure serve [full path to where you stored the files] - Should match your --alluredir parm
