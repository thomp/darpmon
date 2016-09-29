# darpmon

*Monitor presence of devices on a local network

---

**darpmon** periodically scans the local network and logs the presence of devices on the network.

## Installation

To install darpmon from source, change to the directory where setup.py is located.

```python setup.py install```

## Use

To run darpmon, you can simply execute:

   darpmon

For extended monitoring, consider something like:

   nohup darpmon > /dev/null &

To analyze the darpmon log, execute:

   dmparse


## Configuration

You can configure darpmon by editing ~/.darpmon.json. An example is included the darpmon source code.
