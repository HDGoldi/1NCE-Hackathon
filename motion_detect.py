from sense_hat import SenseHat

sense = SenseHat()

red = (255, 0, 0)

while True:
	acceleration = sense.get_accelerometer_raw()
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['z']

	x = abs(x)
	y = abs(y)
	z = abs(z)
	
	if x > 1.5 or y > 1.5 or z > 1.5:
		sense.show_letter("!", red)
		print("Movemet detected!")
	else:
		sense.clear()
