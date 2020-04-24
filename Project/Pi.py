import pygame
from gpiozero import LED
from gpiozero import Button
import importlib.util
import RPi.GPIO as GPIO
import threading
import time
import api
vehicle_id = "V-1"
check = 0
sender = "vehicle"

token = "bqHtyXYfQWvCL9mHXpNdnEQesD0bh9Nr"

states_dic = {"carLock": True, "carOn": True, "defrost": {"back": True, "front": True}, "seatHeater": {"bDriver": True, "bPass": True, "fDriver": True, "fPass": True}}
light_dic = {"spicylight1": False, "spicylight2": False}
        
def light18(channel, light_dic, check):
    
    if check == 0:
        light_dic["spicylight1"] = False
        
    
    if check == 1:
        if not light_dic["spicylight1"]:
            light_dic["spicylight1"] = True
            print("the light is on")
            #time.slee
        else:
            light_dic["spicylight1"] = False
            print("the light is off")

    if check == 2:
        light_dic["spicylight1"] = True

def pushbutton24(channel, states_dic):
    check = 0
    #for i in range(2):
    #    print(GPIO.input(24))
    #    print(GPIO.input(23))
    #    print(GPIO.input(25))
    #    if(GPIO.input(24)):
    #        check +=1
    if check == 0:    
        if not states_dic["carLock"]:
            states_dic["carLock"] = True
            print("Button was pressed! Car Locked!")
        else:
            states_dic["carLock"] = False
            print("Button was pressed! Car Unlocked")
        api.set_val(vehicle_id, 'carLock', states_dic["carLock"], sender, token)
    
# If only 1 lvl then use key, if 2 then use subkey as changer
def pushbutton23(channel, states_dic):
    check = 0
    #for i in range(2):
    #   print(GPIO.input(24))
     #   print(GPIO.input(23))
    #    print(GPIO.input(25))
    #    if(GPIO.input(23)):
    #        check +=1
    if check == 0:    
        if not states_dic["seatHeater"]["fPass"]:
            states_dic["seatHeater"]["fPass"] = True
            print("Button was pressed! Car Front passenger seatwarmer on!")
        else:
            states_dic["seatHeater"]["fPass"] = False
            print("Button was pressed! Car Front passenger seatwarmer off!")
        api.set_val(vehicle_id, 'seatHeater', states_dic["seatHeater"]["fPass"], sender, token, subkey='fPass')
        
def pushbutton25(channel, states_dic):    
        if not states_dic["front"]:
            states_dic["front"] = True
            print("Button was pressed! Front Defrost on!")
        else:
            states_dic["front"] = False
            print("Button was pressed! Front Defrost off!")
        api.set_val(vehicle_id, 'defrost', states_dic["front"], sender, token, subkey='front')

class Spicy:
    def __init__(self):
        threading.Thread(target=self.app_input).start()
        threading.Thread(target=self.timer).start()
        threading.Thread(target=self.lighttimer).start()
            
    def app_input(self):
        from subscriber import Subscriber
        print("Went in the thread!")
        project_id = "pub-sub132608"
        subscriber = "sub_asdfjfdklsjdjdyebv_V-1"
        sub = Subscriber(project_id,subscriber,"")
        sub.start_server()
    
    def timer(self):
        z = 1
        x = set()
        timer =[0,0]
        test = 0
        while(z == 1):
            if states_dic["defrost"]["front"] and "states_dic[defrost][front]" not in x:
                x.add("states_dic[defrost][front]")
                print("Timer for Front defrost started!")
                timer[0] = 60
            if timer[0] < 1 and "states_dic[defrost][front]" in x:
                states_dic["defrost"]["front"] = False
                print("Timer for Front defrost ended!")
                x.remove("states_dic[defrost][front]")
                
            if states_dic["defrost"]["back"] and "states_dic[defrost][back]" not in x:
                x.add("states_dic[defrost][back]")
                print("Timer for Back defrost started!")
                timer[1] = 60
            if timer[1] < 1 and "states_dic[defrost][back]" in x:
                states_dic["defrost"]["back"] = False
                print("Timer for Back defrost ended!")
                x.remove("states_dic[defrost][back]")
                
             
            time.sleep(1)
            if timer[0] > 0:
                timer[0] -= 1
            if timer[1] > 0:
                timer[1] -= 1
            test += 1
            #if test == 20:
            #    states_dic["defrost"]["back"] = True
            #if test == 25:
            #    states_dic["defrost"]["front"] = True
        
    def lighttimer(self):
        counter = 1
        print("When into light thread")
        while counter == 1:
            if check == 1:
                for i in range(6):
                    light18(18, light_dic, check)
                    time.sleep(2)
                    print("hello")
                check = 2
            if check == 2:
                light18(18, light_dic, check)
                time.sleep(15)
                check = 0
            if check == 0:
                light18(18, light_dic, check)
                
    def now_running(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=lambda xx: pushbutton24(24, states_dic), bouncetime=300)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=lambda xx: pushbutton23(23, states_dic), bouncetime=300)
        GPIO.add_event_detect(25, GPIO.FALLING, callback=lambda xx: pushbutton25(25, states_dic["defrost"]), bouncetime=300)
        
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
            if light_dic["spicylight1"]:
                GPIO.output(18, GPIO.HIGH)
            else:
                GPIO.output(18, GPIO.LOW)
            if light_dic["spicylight2"]:
                GPIO.output(17, GPIO.HIGH)
            else:
                GPIO.output(17, GPIO.LOW)
            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                pygame.display.update()
            counter += 1
        
