
## niconico
* using tkinter show text and image which are flowing right to left and 

## pipenv basic commands

In generally, `Pipfile`and`Pipfile.lock` are used for version control such as bundler, composer, npm, cargo, yarn, etc.

On macos install pipenv 
```sh
brew install pipenv
```

if pipfile exists, file inside packages will be installed
```sh
pipenv install
```

Add the package to a your project
```sh
pipenv install <package>
```

### requirement.txt

If you only have a requirements.txt file when you run pipenv install, Pipenv will automatically import the contents of that file and create a Pipfile.

install from requirement.txt
```sh
pipenv install -r requirements.txt
```

### other commands

* `pipenv --three`  create pipfile
* `pipenv lock -r`  check local packages
* `pipenv check`    check security vulnerabilities
* `pipenv graph`    check dependency graph

