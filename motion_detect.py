from sense_hat import SenseHat
import boto3

# Create an SNS client
sns = boto3.client('sns')

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
		response = sns.publish(
			TopicArn='arn:aws:sns:eu-central-1:779684591593:motion-detect-1',
			Message='A new motion on Device 1 was detected.',
		)
		print(response)
	else:
		sense.clear()
