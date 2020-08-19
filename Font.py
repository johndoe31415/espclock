from UDisplay import UDisplay

glyphs = {
	" ": UDisplay.create_glyph(width = 0, height = 0, xoffset = 0, yoffset = 0, xadvance = 6, data = bytes()),
	":": UDisplay.create_glyph(width = 1, height = 7, xoffset = 1, yoffset = -7, xadvance = 3, data = bytes((0x24, ))),
	"0": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x3e, 0x51, 0x49, 0x45, 0x3e))),
	"1": UDisplay.create_glyph(width = 3, height = 7, xoffset = 2, yoffset = -7, xadvance = 6, data = bytes((0x42, 0x7f, 0x40))),
	"2": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x62, 0x51, 0x49, 0x49, 0x46))),
	"3": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x22, 0x41, 0x49, 0x49, 0x36))),
	"4": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x18, 0x14, 0x12, 0x11, 0x7f))),
	"5": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x27, 0x45, 0x45, 0x45, 0x39))),
	"6": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x3e, 0x49, 0x49, 0x49, 0x32))),
	"7": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x01, 0x71, 0x09, 0x05, 0x03))),
	"8": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x36, 0x49, 0x49, 0x49, 0x36))),
	"9": UDisplay.create_glyph(width = 5, height = 7, xoffset = 0, yoffset = -7, xadvance = 6, data = bytes((0x26, 0x49, 0x49, 0x49, 0x3e))),
}
