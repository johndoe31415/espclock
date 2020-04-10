# espclock
This is a wall clock that connects to an ESP32, which runs Micropython and
performs NTP requests. The libraries to perform timestamp to datetime
conversions are native Python libs, as is the NTP client. I'm using an
ESP32-WROOM. There is some code to support a dot matrix display, but I ended up
hacking a previously existing radio clock and inject a mock DCF77 signal into
that clock.

## Installations
First, install esptool to flash the ESP32:

```
pip3 install esptool webrepl
```

Then, [download Micropython](https://micropython.org/download#esp32) and flash it on the ESP:

```
$ esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
$ esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-idf3-20191220-v1.12.bin
```

The serial console can be connected to using picocom using 115200 8N1. To enable WiFi manually, run:

```
import network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("essid", "psk")
```

Initially, webrepl needs to be setup once:

```
import webrepl_setup
```

Then, the files can be pushed on the client (using the password you've
specified during webrepl_setup). For example:

```
$ webreplcmd --host 192.168.2.201 --password S0OHcoka put main.py main.py
```


## License
GNU GPL-3.
