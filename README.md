# darpmon

Monitor presence of devices on a local network

---

*darpmon* periodically scans the local network and logs the presence of devices on the network. MAC addresses are used to identify devices.

## Installation

To install darpmon from source, change to the directory where setup.py is located and then execute

`python setup.py install`


## Use

To run darpmon, simply execute `darpmon`.

For extended monitoring, consider something like `nohup darpmon > /dev/null &`


## Configuration

Configure darpmon by editing `~/.darpmon.json`. An example is included in the source code.


## Automatically running darpmon at boot time

To ensure darpmon runs if the system reboots (e.g., a power failure), consider using `cron`. Use `crontab -e` and add a line for running darpmon whenever the sytem boots. Consider something along the lines of

```
@reboot nohup /full/path/to/darpmon > /dev/null &
```
