#### Must run this script with `sudo` ####

from rpi_ws281x import PixelStrip, Color
import time

### LED strip configuration ###
LED_COUNT = 256				# Number of LED pixels.
LED_PIN = 18				# GPIO pin connected to the pixels (Uses PWM. This is physical pin 12.). GPIO 18 is the default pin for PWM.
LED_FREQ_HZ = 800000		# LED signal frequency in Hertz (usually 800kHz).
LED_DMA = 10				# DMA channel to use for generating signal (try 10).
LED_BRIGHTNESS = 25			# Set to '0' for off and '255' for ultra-brightness. '25' is good for testing purposes.
LED_CHANNEL = 0				# Set to '1' for GPIO 13 (This is physical pin 13).
LED_INVERT = False			# Set to 'True' to invert the signal (when using NPN transistor level shift).


""" Initialize the LED strip. """
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


""" Function to retrieve the LED index based on row and column. """
def get_led_index(row, col):

	# Converting 2D coordinates into a 1D LED strip index.
	lookup_table = [
		[0, 15, 16, 31, 32, 47, 48, 63, 64, 79, 80, 95,  96, 111, 112, 127, 128, 143, 144, 159, 160, 175, 176, 191, 192, 207, 208, 223, 224, 239, 240, 255],
		[1, 14, 17, 30, 33, 46, 49, 62, 65, 78, 81, 94,  97, 110, 113, 126, 129, 142, 145, 158, 161, 174, 177, 190, 193, 206, 209, 222, 225, 238, 241, 254],
		[2, 13, 18, 29, 34, 45, 50, 61, 66, 77, 82, 93,  98, 109, 114, 125, 130, 141, 146, 157, 162, 173, 178, 189, 194, 205, 210, 221, 226, 237, 242, 253],
		[3, 12, 19, 28, 35, 44, 51, 60, 67, 76, 83, 92,  99, 108, 115, 124, 131, 140, 147, 156, 163, 172, 179, 188, 195, 204, 211, 220, 227, 236, 243, 252],
		[4, 11, 20, 27, 36, 43, 52, 59, 68, 75, 84, 91, 100, 107, 116, 123, 132, 139, 148, 155, 164, 171, 180, 187, 196, 203, 212, 219, 228, 235, 244, 251],
		[5, 10, 21, 26, 37, 42, 53, 58, 69, 74, 85, 90, 101, 106, 117, 122, 133, 138, 149, 154, 165, 170, 181, 186, 197, 202, 213, 218, 229, 234, 245, 250],
		[6,  9, 22, 25, 38, 41, 54, 57, 70, 73, 86, 89, 102, 105, 118, 121, 134, 137, 150, 153, 166, 169, 182, 185, 198, 201, 214, 217, 230, 233, 246, 249],
		[7,  8, 23, 24, 39, 40, 55, 56, 71, 72, 87, 88, 103, 104, 119, 120, 135, 136, 151, 152, 167, 168, 183, 184, 199, 200, 215, 216, 231, 232, 247, 248]
	]

	return lookup_table[row][col]


""" Function to set the parameters of a specific region on the LED panel and the color for it. """
def set_pixel_color(top_pixel, bottom_pixel, color):
	for row in range(top_pixel[0], bottom_pixel[0] + 1):
		for col in range(top_pixel[1], bottom_pixel[1] + 1):
			index = get_led_index(row, col)
			strip.setPixelColor(index, color)

""" Function to clear the entire grid by turning off all LEDs. """
def clear_grid():
	for row in range(8):											# 8 rows as per lookup_table.
		for col in range(32):										# 32 columns as per lookup_table.
			index = get_led_index(row, col)
			strip.setPixelColor(index, Color(0, 0, 0))


#==========================================================================================================================================================================#
""" Main program to animate a sequential right turn signal. """
def main():
	pixel_color = Color(255, 70, 0)									# Define the color. (Orange)

	while True:
		for col_start in range(0, 32):								# Iterating over each column left-to-right.

			""" Define the column's top and bottom pixel coordinates (row, column). """
			top_pixel = (0, col_start)
			bottom_pixel = (3, col_start)							# Since only one column is being lit up, the ending column is the same as the starting column.

			set_pixel_color(top_pixel, bottom_pixel, pixel_color)	# Set the color of the column defined by top_pixel and bottom_pixel coordinates.

			strip.show()											# Display the pixels.
			time.sleep(0.015)										# How fast the columns light up in milliseconds. Lower number = faster.

		time.sleep(0.2)												# How long the LEDs stay on in milliseconds before turning off. Lower number = faster.

		clear_grid()												# Clear the grid before starting the sequence again.
		strip.show()												# Display the cleared grid.
		time.sleep(0.25)											# How long the LEDs stay off in milliseconds before starting the sequence again. Lower number = faster.

""" Code to handle KeyboardInterrupt """
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		# On a keyboard interrupt, clear the LED strip and exit.
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0, 0, 0))
		strip.show()
		raise SystemExit
