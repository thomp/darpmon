# darpmon

Monitor presence of devices on a local network

---

*darpmon* periodically scans the local network and logs the presence of devices on the network. MAC addresses are used to identify devices.

## Installation

To install darpmon from source, change to the directory where setup.py is located and then execute

`python setup.py install`


## Use

To run darpmon, simply execute `darpmon`. For extended monitoring, consider something like `nohup darpmon > /dev/null &`.

An example:

```
$ sudo python ./darpmon/darpmon.py -l 0
Config file /root/.darpmon.json not found
{"mac": "2c:7e:81:ab:60:f4", "d": "1597339285.4", "ipv4": "10.0.0.1"}
{"mac": "00:14:22:94:ea:60", "d": "1597339285.4", "ipv4": "10.0.0.79"}
{"mac": "2c:7e:81:ab:60:f5", "d": "1597339285.4", "ipv4": "10.0.0.254"}
{"mac": "2c:7e:81:ab:60:f4", "d": "1597339348.0", "ipv4": "10.0.0.1"}
{"mac": "00:14:22:94:ea:60", "d": "1597339348.0", "ipv4": "10.0.0.79"}
{"mac": "2c:7e:81:ab:60:f5", "d": "1597339348.0", "ipv4": "10.0.0.254"}
{"mac": "2c:7e:81:ab:60:f4", "d": "1597339410.6", "ipv4": "10.0.0.1"}
{"mac": "00:14:22:94:ea:60", "d": "1597339410.6", "ipv4": "10.0.0.79"}
{"mac": "2c:7e:81:ab:60:f5", "d": "1597339410.6", "ipv4": "10.0.0.254"}
{"mac": "2c:7e:81:ab:60:f4", "d": "1597339473.19", "ipv4": "10.0.0.1"}
{"mac": "00:14:22:94:ea:60", "d": "1597339473.19", "ipv4": "10.0.0.79"}
{"mac": "2c:7e:81:ab:60:f5", "d": "1597339473.19", "ipv4": "10.0.0.254"}
```



## Configuration

Configure darpmon by editing `~/.darpmon.json`. An example is included in the source code.


## Automatically running darpmon at boot time

To ensure darpmon runs if the system reboots (e.g., a power failure), consider using `cron`. Use `crontab -e` and add a line for running darpmon whenever the sytem boots. Consider something along the lines of

```
@reboot nohup /full/path/to/darpmon > /dev/null &
```
