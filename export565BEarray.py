#!/usr/bin/python
from gimpfu import register, PF_IMAGE, PF_DRAWABLE, PF_STRING, PF_OPTION, main,gimp
import os

def encodeColor(data):
	# Shift and mask the bits to transform three 8-bit values into one 16 bit
	# Then put it in BE order as individual bytes
	twoByte = (ord(data[0]) << 8) & 0xf800 | (ord(data[1]) << 3) & 0x07e0 | (ord(data[2]) >> 3)
	return "0x"+format((twoByte & 0xff00) >> 8,"02X") + ", " + "0x"+format(twoByte & 0xff,"02X") 

def export565array(timg, tdrawable, filename):
	pr =tdrawable.get_pixel_rgn(0, 0, timg.width,timg.height, False, False);
	i=0
	j=0
	count=0
	size = timg.width*timg.height
	# Header comment
	output = "/* C header of image exported from gimp - 565 Big Endian format */\n\n" 
	output += "static const struct\n{\n\tuint32_t width;\n\tuint32_t height;\n\t"
	output += "uint8_t pixel_data["+str(timg.width)+"*"+str(timg.height)+"*2];\n"
	output += "} gimp_image = {\n  "
	output += str(timg.width)+",\n  "
	output += str(timg.height)+",\n  {\n"

	while (j<timg.height):
		while (i<timg.width):
			output += encodeColor(pr[i,j]) + ", "
			i+=1
			if count % 8 == 7:
				output +="\n"
			count += 1
		j+=1
		i=0
	output += "\n}};"
	if "~" in filename:
		filename = os.path.expanduser(filename)
	savefile = open(filename,"w")
	savefile.write(output)
	savefile.close() 


register(
		"export565BE",
		"Saves image data to C source in RGB565 Big-endian format",
		"Saves image data to C source in RGB565 Big-endian format",
        "Sean Mollet",
		"Sean Mollet",
		"2020",
		"<Image>/File/Export565BE",
		"RGB*, GRAY*, INDEXED*",
		[
		(PF_STRING,"filename","file to save code to","untitled.c"),
		],
		[],#no return params from the plugin function
		export565array)

main()
