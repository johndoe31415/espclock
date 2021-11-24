configuration = {
	"comment": "Copy this file to 'Configuration.py', set the ESSID and psk and push it on the ESP.",
	"wifi": {
		"essid":	"local-wifi-essid",
		"psk":		"local-wifi-psk",
	},
	"ntp_server":			"pool.ntp.org",
	"mode":					"dcf77",				# dcf77 or spi_max7219_32x8
	"timezone":				"Europe/Berlin",		# Currently supports only UTC or Europe/Berlin
	"max7219_brightness":	0,						# Only relevant in MAX7219 mode
}
