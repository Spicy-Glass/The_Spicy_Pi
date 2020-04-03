import pygame
from gpiozero import LED
from gpiozero import Button
import importlib.util
import RPi.GPIO as GPIO
import threading
import time
import api

states_dic = {"carLock": True, "carOn": True, "defrost": {"back": True, "front": True}, "seatHeater": {"bDriver": True, "bPass": True, "fDriver": True, "fPass": True}}

def pushbutton1(channel, states_dic):
    if not states_dic["carLock"]:
        states_dic["carLock"] = True
        print("Button was pressed! Car Locked!")
    else:
        states_dic["carLock"] = False
        print("Button was pressed! Car Unlocked")
    api.set_val(vehicle_id, 'carLock', states_dic["carLock"], sender, token)
    
# If only 1 lvl then use key, if 2 then use subkey as changer
def pushbutton2(channel, states_dic):
    if not states_dic["seatHeater"]["fPass"]:
        states_dic["seatHeater"]["fPass"] = True
        print("Button was pressed! Car Front passenger seatwarmer on!")
    else:
        states_dic["seatHeater"]["fPass"] = False
        print("Button was pressed! Car Front passenger seatwarmer off!")
    api.set_val(vehicle_id, 'seatHeater', states_dic["seatHeater"]["fPass"], sender, token, subkey='fPass')
        
def pushbutton3(channel, states_dic):
    if not states_dic["defrost"]["front"]:
        states_dic["defrost"]["front"] = True
        print("Button was pressed! Front Defrost on!")
    else:
        states_dic["defrost"]["front"] = False
        print("Button was pressed! Front Defrost off!")
    api.set_val(vehicle_id, 'defrost', states_dic["defrost"]["front"], sender, token, subkey='front')


class Spicy:
    def __init__(self, test):
        self.test = test
        threading.Thread(target=self.app_input).start()
        
    def app_input(self):
        from subscriber import Subscriber
        print("Went in the thread!")
        sub = Subscriber(project_id,subscriber,"")
        sub.start_server()
    

    def now_running(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=lambda xx: pushbutton1(23, states_dic), bouncetime=300)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=lambda xx: pushbutton2(24, states_dic), bouncetime=300)
        GPIO.add_event_detect(25, GPIO.FALLING, callback=lambda xx: pushbutton3(25, states_dic), bouncetime=300)
        
        pygame.init()

        white = (255, 255, 255)

        x = 1000
        y = 600

        display_surface = pygame.display.set_mode((x, y))

        pygame.display.set_caption('Spicy Car')

        image_car = pygame.image.load(r'/home/pi/Documents/Project/Images/car.jpg')
        image_chair_on = pygame.image.load(r'/home/pi/Documents/Project/Images/chair_on.jpg')
        image_chair_off = pygame.image.load(r'/home/pi/Documents/Project/Images/chair_off.jpg')
        image_fire_on = pygame.image.load(r'/home/pi/Documents/Project/Images/fire.jpg')
        image_fire_off = pygame.image.load(r'/home/pi/Documents/Project/Images/fire_off.jpg')
        image_lock = pygame.image.load(r'/home/pi/Documents/Project/Images/lock.jpg')
        image_unlock = pygame.image.load(r'/home/pi/Documents/Project/Images/unlock.jpg')
        image_on = pygame.image.load(r'/home/pi/Documents/Project/Images/on.jpg')
        image_off = pygame.image.load(r'/home/pi/Documents/Project/Images/off.jpg')

        # infinite loop
        counter = 0
        while True:
            display_surface.fill(white)
            
            # How each state is processed
            display_surface.blit(image_car, (200, 100))

            if states_dic["carLock"]:
                display_surface.blit(image_lock, (440, 100))
            else:
                display_surface.blit(image_unlock, (440, 100))
                
            if states_dic["carOn"]:
                display_surface.blit(image_on, (500, 505))
            else:
                display_surface.blit(image_off, (500, 505))
                
            if states_dic["seatHeater"]["fDriver"]:
                display_surface.blit(image_chair_on, (0, 0))
            else:
                display_surface.blit(image_chair_off, (0, 0))
            if states_dic["seatHeater"]["fPass"]:
                display_surface.blit(image_chair_on, (100, 0))
            else:
                display_surface.blit(image_chair_off, (100, 0))
            if states_dic["seatHeater"]["bDriver"]:
                display_surface.blit(image_chair_on, (0, 100))
            else:
                display_surface.blit(image_chair_off, (0, 100))
            if states_dic["seatHeater"]["bPass"]:
                display_surface.blit(image_chair_on, (100, 100))
            else:
                display_surface.blit(image_chair_off, (100, 100))
                
            if states_dic["defrost"]["back"]:
                display_surface.blit(image_fire_on, (300, 250))
            else:
                display_surface.blit(image_fire_off, (300, 250))
            if states_dic["defrost"]["front"]:
                display_surface.blit(image_fire_on, (650, 250))
            else:
                display_surface.blit(image_fire_off, (650, 250))
            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                pygame.display.update()
            counter += 1
        
