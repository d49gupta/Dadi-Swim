import RPi.GPIO as GPIO
import time

# Define GPIO pin for fan control (e.g., GPIO 14)
FAN_PIN = 14

# Set GPIO pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Function to control fan speed using PWM
def set_fan_speed(speed):
    """
    Controls the fan speed using PWM.

    Args:
        speed: An integer between 0 and 100 representing the fan speed percentage.
    """
    if speed < 0 or speed > 100:
        raise ValueError("Speed must be between 0 and 100")

    pwm.ChangeDutyCycle(speed)

# Example usage:
try:
    # Initialize PWM on the fan pin
    pwm = GPIO.PWM(FAN_PIN, 25000)  # Frequency of 25 kHz
    pwm.start(0)  # Start with 0% duty cycle (fan off)

    while True:
        # Get current temperature (replace with your method)
        temperature = get_cpu_temperature()

        # Determine fan speed based on temperature (example logic)
        if temperature > 60:
            fan_speed = 100
        elif temperature > 50:
            fan_speed = 50
        else:
            fan_speed = 0

        # Set the fan speed
        set_fan_speed(fan_speed)

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    pwm.stop()
    GPIO.cleanup()
