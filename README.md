# tptester
task-point tester

## Intro
* Task-point tester, N tasks and M points = N*M tests matrix
* Lightweight, simple python script with no dependency
* Config with json

## Usage
In a repo tree
```
your repo
|-- src
|-- build
|-- ...
|-- tests
    |-- testpoint1
        |-- something for test
    |-- tp2
        |-- something for test
    |-- awd
        |-- something for test
    |-- ...
```

Setup tptester

```console
$ cd tests
$ git submodule add --name tptester https://github.com/TitanSnow/tptester.git tptester
```

Write tasklists saved to `.test.json`. For example:

```json
{
    "generic":{
        "steps":[
            ["xmake","f","-c","-P",null,"-v","--backtrace"],
            ["xmake","-P",null,"-v","--backtrace"],
            ["xmake","p","-P",null,"-v","--backtrace"]
        ]
    },

    "iphoneos":{
        "platform":"darwin",
        "steps":[
            ["xmake","m","-P",null,"package","-p","iphoneos"]
        ]
    }
}
```

Only task *`generic`* will run on every testpoint by default. A *`null`* in a step will be replaced by the name of the testpoint. The *`platform`* has same values as `sys.platform` in python. Only the tasks that match the platform of test environment will be run

Now your tree is like this:
```
your repo
|-- src
|-- build
|-- ...
|-- tests
    |-- testpoint1
        |-- something for test
    |-- tp2
        |-- something for test
    |-- awd
        |-- something for test
    |-- ...
    |-- .test.json
```

Next, add addition info for some testpoints saved to `testpoint/.test.json`. For example, add special platform and/or tasks:

```json
{
    "tasks":["generic","iphoneos"],
    "platform":"darwin"
}
```

Now your tree is like this:
```
your repo
|-- src
|-- build
|-- ...
|-- tests
    |-- testpoint1
        |-- .test.json
        |-- something for test
    |-- tp2
        |-- something for test
    |-- awd
        |-- .test.json
        |-- something for test
    |-- ...
    |-- .test.json
```

All is done! run `python3 tptester/__init__.py` in dir `tests` to auto run the tests!

To add it to your CI scripts like `.travis.yml` just need to add one line:
```yaml
  - python3 -c '__import__("os").chdir("tests");__import__("tptester").auto_test()'
```

Make sure there's python3
