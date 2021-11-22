from Health import controller as controller
import random

while True:
    pulse = random.uniform(60,80)
    temperature = random.uniform(37,37.4)
    temperature = float(str(temperature)[0:5])
    controller.update_user_health_status(1,pulse,temperature)

