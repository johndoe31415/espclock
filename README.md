# espclock
This is a wall clock that connects to an ESP32, which runs MicroPython and
performs NTP requests. The libraries to perform timestamp to datetime
conversions are native Python libs, as is the minimal NTP client. I'm using an
ESP32-WROOM. espclock can either support a 32x8 dot matrix display (using four
MAX7219 drivers), or it can emulate a fake DCF77 signal to inject to upgrade an
existing clock.


## Modes and Hardware
espclock can run in two different modes with different hardware settings:

  * `dcf77`: Emulate a DCF77 (German time clock) signal. Can be used to upgrade
    clocks who use a DCF77 signal input to NTP over Wi-Fi. Essentially,
    emulates a clean digital DCF77 signal that can be directly fed into the
    original clock's decoder circuit.
  * `spi_max7219_32x8`: Connect 4 x MAX7219 that each have 8x8 dot matrix
    connected to the ESP32 via SPI. Shows the time in hh:mm format.
 
The hardware pins that are used in these modes are, respectively:

  * `dcf77` mode:
    - Encoded DCF77 signal output: GPIO15
    - Status LED: GPIO2
  * `spi_max7219_32x8` mode:
    - !CS: GPIO12
    - MOSI: GPIO13
    - SCK: GPIO14

## Installation of MicroPython
First, install esptool to flash the ESP32:

```
pip3 install esptool webrepl
```

Then, [download MicroPython](https://micropython.org/download#esp32) and flash it on the ESP:

```
$ esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
$ esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-idf3-20191220-v1.12.bin
```

Note: For some reason, I'm seeing spurious errors using
`esp32-20210902-v1.17.bin`. In particular, sometimes the !CS GPIO does not
initialize properly and gets "stuck" in the LOW output (possibly also High-Z,
not sure).  I've debugged this issue for quite a while until I realized the
code was fine and it's MicroPython which is misbehaving for whatever reason.
Since I don't think filing a bug makes a lot of sense, I've reverted back to
MicroPython version `esp32-idf3-20191220-v1.12.bin` and everything works
flawlessly with that version.


## Configuration of espclock
There is a configuration file, "Configuration.py" which you need to create to
let espclock know what it should do. Here's the `Configuration_template.json`
file:

```python
configuration = {
	"comment": "Copy this file to 'Configuration.py', set the ESSID and psk and push it on the ESP.",
	"wifi": {
		"essid":	"local-wifi-essid",
		"psk":		"local-wifi-psk",
	},
	"ntp_server":	"pool.ntp.org",
	"mode":			"dcf77",				# dcf77 or spi_max7219_32x8
}
```

You need to set ESSID and PSK of your local WiFi. Then you need to configure
the `mode` to be either `dcf77` or `spi_max7219_32x8`.


## Bringing up the Wi-Fi
The serial console of MicroPython can be connected to using picocom using 115200 8N1:

```
$ picocom --baud 115200 /dev/ttyUSB0
```

To find out the commands to enable the network, you can simply perform

```
$ ./install -p
import network; wifi = network.WLAN(network.STA_IF); wifi.active(True); wifi.connect("essid", "psk")
```

You then need to copy/paste these commands into your picocom console.

To enable WiFi manually, here are the commands again, prettier:

```python
import network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("essid", "psk")
```

Initially, webrepl needs to be setup once:

```python
import webrepl_setup
```

To find out the IP your ESP32 has gotten, use the ifconfig method:

```
print(wifi.ifconfig())
```

## Installing espclock
After setting up webrepl and configuring Wi-Fi manually, you are now ready to
push the espclock files on your ESP32. For this you need to confgure the push
file `push_config.json`.  Copy `push_config_template.json` to
`push_config.json` and edit it (IP address of the device from the `ifconfig()`
call previously as well as the Webrepl password you have chosen). Then you can
install the software by running:

```
$ ./install
```

After reboot, your ESP32 should be running espclock.


## License
GNU GPL-3.
