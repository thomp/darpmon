# darpmon

*Monitor presence of devices on a local network

---

**darpmon** periodically scans the local network and logs the presence of devices on the network.

## Installation

To install darpmon from source, change to the directory where setup.py is located.

```python setup.py install```


## Use

To run darpmon, you can simply execute `darpmon`. For extended monitoring, consider something like:

   nohup darpmon > /dev/null &


## Configuration

You can configure darpmon by editing ~/.darpmon.json. An example is included the darpmon source code.


## Automatically running darpmon at boot time

If you'd like darpmon to run if the system reboots (e.g., a power failure), consider using cron.

```
su

crontab -e
```

Then add a line for running darpmon whenever the sytem boots:

```
@reboot nohup /full/path/to/darpmon > /dev/null &
```
