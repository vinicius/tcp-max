# TCP MAX 

A basic program to calculate the TCP maximum flow between nodes in a network.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 2.7 or higher

### Installing

Just download the repository inside a directory of your choice.

## Running the tests

To run the unit tests, enter the root directory of the repository and run the test suite file:

python test_suite.py

## Running the program 

To run the program, enter the root directory of the repository and run the main file. A text file with the description of the network must be passed as argument:

python main.py my_network_description.txt

### Network description

The network must be descripted using the following model:

```
# Links section
link <label1>
link <label2>
...

# Nodes section
node X <upload> <download> <incoming_links> <oucoming_links>
...
```

The links must contain the label of the links between the nodes.
The nodes must contain the node name, followed by the download and upload available bandwith and finally the incoming and the oucoming connections.
Lines starting with # or empty ones are ignored.

Example:

```
link AB
link AC
link BC

node A 100 1000 [] [AB,AC]
node B 100 10000 [AB] [BC]
node C 1000 150 [AC,BC] []
```

In the example above, we have 3 connections, the first one (AB) between the node A and B, the second one (AC) between node A and C and the third one between B and C.
The node A has 100kbps upload and 10000kbps download bandwith. There is not incoming connections and two outcoming connections, AB and BC. The nodes B and C follows the same model.

## Built With

* [Python](https://www.python.org) - Python language
* [Pydoc](https://docs.python.org/2/library/pydoc.html) - Doc generator

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Vinicius G Pinheiro** - *Initial work* - [Vinicius](https://github.com/vinicius)