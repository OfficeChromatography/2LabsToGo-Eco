from datetime import datetime
from app.settings import STATIC_ROOT, MEDIA_ROOT
import os
import re
import glob
import pytz         #Import Timezone Library
from connection.forms import OC_LAB
from picamera2 import Picamera2, Metadata
import time
import libcamera
from libcamera import controls

tz = pytz.timezone('Europe/Berlin') #Setting Timezone for Berlin


class Camera:
    @classmethod 

    def __init__(self):
        self.picam2 = Picamera2()
 
    def shoot(self, format, num_pict, dtime):
        '''Takes pictures with the camera and saves them to the local file system.
        It takes three arguments: format, num_pict, and dtime.
        format is the file format of the pictures (jpg, png, etc.),
        num_pict is the number of pictures to take,
        dtime is the delay time between images.'''
        time.sleep(2)
        self.picam2.start()
        time.sleep(5)
        format = format.lower()
        name = self.create_time_stamp()
        time.sleep(1)
        metadata = self.picam2.capture_metadata()
        photo_path = []
        i=0
        for i in range(num_pict):
            if num_pict > 1:
                self.picam2.set_controls({"AeEnable": False})
                time.sleep(30)
                print("metadata 1:", " ExposureTime ", metadata["ExposureTime"], " ColourGains ", metadata["ColourGains"], " AnalogueGain ", metadata["AnalogueGain"])
                
            else:
                print("metadata 1:", " ExposureTime ", metadata["ExposureTime"], " ColourGains ", metadata["ColourGains"], " AnalogueGain ", metadata["AnalogueGain"])
            self.picam2.capture_file(f'{name}{i}.{format}')
            request = self.picam2.capture_request()
            metadata = request.get_metadata()
            request.release()
            print("metadata 2:", " ExposureTime ", metadata["ExposureTime"], " ColourGains ", metadata["ColourGains"], " AnalogueGain ", metadata["AnalogueGain"])

            os.path.exists(f'{name}{i}.{format}')
            photo_path.append(os.getcwd() + '/' + name + str(i) + '.' + format)
            time.sleep(1)
            i += 1
            time.sleep(dtime)
        time.sleep(5)
        self.picam2.stop()
        self.picam2.close()
        return photo_path

    def create_time_stamp(self):
        '''Creates a timestamp in the format "YYYY.MM.DD-HH.MM.SS".'''
        return datetime.now(tz).strftime("%Y.%m.%d-%H.%M.%S")

    def set_camera_control(self, control, value):
        '''Sets a camera control based on the control and value arguments.
        The only control supported is 'auto_exposure'.'''
        if((control == 'auto_exposure')):
            if (value == 1):
                self.picam2.set_controls({"AeEnable": True})
            elif (value == 0):
                self.picam2.set_controls({"AeEnable": False})
            time.sleep(1)

    def set_camera_property_awb(self, mode, value):
        '''Sets a camera property based on the mode and value arguments.
        The only mode supported is 'white_balance_auto_preset'.'''
        if((mode == 'white_balance_auto_preset')):
            if((value == 0)):
                self.picam2.set_controls({"AwbEnable": False})
            else:
                self.picam2.set_controls({"AwbMode": value})
                
    
    def set_camera_property_colour_gains(self, property, value):
        '''Sets a camera property based on the property and value arguments.
        The only property supported is 'colour_gains'.'''
        if((property == 'colour_gains')):
            value = value.split(',')
            self.picam2.set_controls({"ColourGains": (float(value[0]),float(value[1]))})

    def set_camera_property(self, property, value):
        '''Sets a camera property based on the property and value arguments.
        The supported properties are 'exposure_time_absolute',
        'analogue_gain', 'brightness', 'contrast', 'saturation', and 'sharpness'.'''
        if((property == 'exposure_time_absolute')):
            self.picam2.set_controls({"ExposureTime": int(value*1000000)})

        if((property == 'analogue_gain')):
            self.picam2.set_controls({"AnalogueGain": value})

        if((property == 'brightness')):
            self.picam2.set_controls({"Brightness": value})

        if((property == 'contrast')):
            self.picam2.set_controls({"Contrast": value})

        if((property == 'saturation')):
            self.picam2.set_controls({"Saturation": value})

        if((property == 'sharpness')):
            self.picam2.set_controls({"Sharpness": value})                

    def set_resolution(self):
        '''Sets the camera's resolution to 2028x1520.'''
        camera_conf = self.picam2.create_still_configuration(main={"size": (2028, 1520)})
        camera_conf["transform"] = libcamera.Transform(hflip=1, vflip=1)
        self.picam2.configure(camera_conf)
    
    def wait_until_controls_applied(self, target_exposure_us=None, target_gain=None, timeout=2.0, tolerance=0.05):
        t_start = time.time()
        while time.time() - t_start < timeout:
            metadata = self.picam2.capture_metadata()
            real_exp = metadata.get("ExposureTime", 0)
            real_gain = metadata.get("AnalogueGain", 0)
    
            ok_exp = ok_gain = True
    
            if target_exposure_us is not None:
                if abs(real_exp - target_exposure_us) > tolerance * target_exposure_us:
                    ok_exp = False
    
            if target_gain is not None:
                if abs(real_gain - target_gain) > tolerance * target_gain:
                    ok_gain = False
    
            if ok_exp and ok_gain:
                return
    
            time.sleep(0.1)
    
        print("⚠️ Waiting time is over. Not all the values were applied.")



class UvLed:
    def __init__(self, pin):
        self.pin = pin

    def set_power(self, power):
        '''Sends a command to turn the LED on or off to the OC_LAB class based
        on the pin and power arguments.'''
        OC_LAB.send_now(f'M42 P{self.pin} S{power}')

class VisibleLed:
    def __init__(self):
        pass

    def set_rgb(self, red_power, green_power, blue_power, white_power):
        '''Sends a command to set the RGBW values of the LED to the OC_LAB class based
        on the red_power, green_power, blue_power, and white_power arguments.'''
        OC_LAB.send_now(f'G93R{red_power}G{green_power}B{blue_power}W{white_power}')
    
