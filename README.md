# demo-automation

Demo with automation techniques

## Docker Image
ppae: python, playwright, allure example

### Prerequisites
Install docker
depending on your installation you may need admin permissions for the following

### Build a new image
from the docker directory run (--no-cache as when we rebuild it we want it to pull a fresh copy of the test repo):
```bash
docker build . -t ppae --no-cache
````

### Final set up:
Start the container (we use privaliged to allow for date manipulation. **NEVER** use it in a prod docker container)
```bash
docker run -it --privileged ppae
````
Run the following commands (so we can use everything installed by linuxbrew) and add our python helpers to our path
```bash 
eval $(~/.linuxbrew/bin/brew shellenv)
export PYTHONPATH=~/ppae/helpers
```

cd into the test dir
```bash
cd ppae
````

Run either of the following to demo the tests:
```bash
./runTestAndDisplayResults.sh
./runTestAndDisplayResultsHistoryExample.sh
````

### Failing tests
Intermittently TestBT14PropertiesAvailable or TestBT16PropertiesAvailable might fail where the number of property's available displayed will not equal the count of properties displayed. I suspect its related to highlighted/promoted properties but given its a public web page, where the api calls return html and nothing has ids its a bit of a hard one to nail down without specs and tests designed to take account of the business requirements that the site was designed against

### Next improvements
Multiple browsers - Playwright is designed to create one single browser for the tests and create individual contexts for each test, for resource and speed purposes. Currently the tests are creating a browser each. Investigate a solution for this (most likely a pytest scoped session browser.)

Parallelism - pytest-parallel breaks the allure reports, investigating the code shows no obvious reason for this. Try xdist. If the same issues persist try running the tests with different browsers at the same time using bash.

Slow-mo -  a headed slowmo demo would be worth showing.

Multiple contexts - a basic chat app could be used to demo this - will require finding or writing one but its an interesting and powerful feature worth demo-ing
