from app.settings import STATIC_ROOT, MEDIA_ROOT
from .forms import ShootConfigurationForm, CameraControlsForm, UserControlsForm, AligmentConfigurationForm, \
    LedsControlsForm
from .models import Images_Db

from finecontrol.forms import Method_Form
from finecontrol.models import Method_Db

from django.core.files import File
from PIL import Image
import PIL.ExifTags
from PIL.ExifTags import TAGS
import time
import subprocess
import os
from datetime import datetime
from os import remove
from os import path

import cv2
import numpy as np

from .Camera import *


def basic_conf():
    basic_conf = {'brightness': 0,
                  'contrast': 0,
                  'saturation': 0,
                  'sharpness': 0,
                  'resolution': '2028x1520',
                  'pixelformat': 2,

                  'auto_exposure': 0,
                  'exposure_time_absolute': 0.025,
                  'white_balance_auto_preset': 1,
                  'analogue_gain': 1,
                  'colour_gains': '1.0,1.0',
                  'imagenumber': 1,
                  'delaytime': 0,

                  'uv365_power': 0,
                  'uv255_power': 0,
                  'whitet_power': 0,
                  'red': 0,
                  'blue': 0,
                  'green': 0,
                  'white': 0,
                  }
    return basic_conf

def get_metadata(image_in_Db):
    img = Image.open("./media/images/best1.jpeg")
    exifdata = img.getexif()
    dic = {}
    img_data = ""
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        img_data += f"{tag}: {data}\n"
        dic[tag] = str(data)
    return filter_data(dic)

def filter_data(data):
    values = ["BrightnessValue", "ImageWidth", "ImageLength", "Model", "ExposureTime",
              "XResolution", "YResolution", "ExposureProgram", "ISOSpeedRatings",
              "ResolutionUnit", "ExifOffset", "ExposureMode", "WhiteBalance"]
    return dict(filter(lambda x: x[0] in values, data.items()))

class PhotoShootManager:
    def __init__(self, request):
        self.camera = Camera()
        self.nm_255 = UvLed(5)
        self.nm_365 = UvLed(2)
        self.whitet = UvLed(13)
        self.visible_leds = VisibleLed()

        self.user = request.user
        self.camera_config_form = CameraControlsForm(request.POST or None)
        self.user_config_form = UserControlsForm(request.POST or None)
        self.format_config_form = ShootConfigurationForm(request.POST or None)
        self.led_config_form = LedsControlsForm(request.POST or None)

        self.id = request.POST.get("selected-element-id")
        self.import_mode = request.session.get('imported_form_data') is not None

        if self.import_mode:
            print("Import mode active: 'selected-element-id' is not required.")
        elif self.id is None:
            print("Error: Method ID is None. Check if 'selected-element-id' is being sent in the request.")
        else:
            print(f"Method ID obtained: {self.id}")

        self.path_photo = []    

    def are_shoot_options_correct(self):
        # Checks the Camera_config, user_Config, the format_config
        # Returns the instance of filled forms
        if all([
            self.camera_config_form.is_valid(),
            self.user_config_form.is_valid(),
            self.format_config_form.is_valid(),
            self.led_config_form.is_valid()
        ]):
            return True
        else:
            print("Form validation errors:")
            print(self.camera_config_form.errors)
            print(self.user_config_form.errors)
            print(self.format_config_form.errors)
            print(self.led_config_form.errors)
            return False

    def set_camera_configurations(self, color_dict):
        if not self.are_shoot_options_correct():
            raise ValueError("One or more forms are not valid.")

        self.visible_leds.set_rgb(
            color_dict['red'],
            color_dict['green'],
            color_dict['blue'],
            self.led_config_form.cleaned_data['white'],
        )

        ae_value = self.camera_config_form.cleaned_data['auto_exposure']

        self.camera.set_camera_control('auto_exposure', ae_value)
        time.sleep(0.5)
        if ae_value == 0:

            try:
                self.camera.picam2.stop()
            except Exception:
                pass  

            self.camera.set_resolution()
            self.camera.picam2.set_controls({"AeEnable": False})
            time.sleep(0.5)  

            for key, value in self.user_config_form.cleaned_data.items():
                self.camera.set_camera_property(key, value)

            for key, value in self.camera_config_form.cleaned_data.items():
                self.camera.set_camera_property(key, value)

                if key == 'white_balance_auto_preset':
                    self.camera.set_camera_property_awb(key, value)
                    if value == 7:
                        for key2, val2 in self.camera_config_form.cleaned_data.items():
                            if key2 == 'colour_gains':
                                self.camera.set_camera_property_colour_gains(key2, val2)

            self.camera.picam2.start()
            time.sleep(0.5)
        else:
            self.camera.set_resolution()
            self.camera.picam2.start()
            time.sleep(0.5)

            self.camera.picam2.set_controls({"AeEnable": True})
            time.sleep(1.5) 
            for i in range(2):
                try:
                    metadata = self.camera.picam2.capture_metadata()
                    print(f"Metadata AE #{i+1}: Exposure={metadata.get('ExposureTime')}, Gain={metadata.get('AnalogueGain')}")
                except Exception as e:
                    print(f"❌ Error AE #{i+1}: {e}")
                time.sleep(0.4)

        self.camera.picam2.stop()
                    
        try:
            self.camera.picam2.stop()
        except Exception as e:
            print("⚠️ Camera could not be stopped.", e)

        self.camera.set_resolution()

    def shoot(self):
        if not self.are_shoot_options_correct():
            raise ValueError("One or more forms are not valid. Cannot perform photo shoot.")
        self.nm_255.set_power(self.led_config_form.cleaned_data['uv255_power'])
        self.nm_365.set_power(self.led_config_form.cleaned_data['uv365_power'])
        self.whitet.set_power(self.led_config_form.cleaned_data['whitet_power'])
        
        file_format = self.format_config_form.cleaned_data['pixelformat']
        image_number = self.camera_config_form.cleaned_data['imagenumber']
        delay_time = self.camera_config_form.cleaned_data['delaytime']

        self.path_photo = self.camera.shoot(file_format, image_number, delay_time)

        self.nm_255.set_power(0)
        self.nm_365.set_power(0)
        self.whitet.set_power(0)
        self.visible_leds.set_rgb(0, 0, 0, 0)

    def save_photo_in_db(self):
        images = []

        if self.id is None and not self.import_mode:
            raise ValueError("The method ID is None. Cannot save photo without a valid method ID.")

        if not self.import_mode:
            try:
                method_instance = Method_Db.objects.get(pk=self.id)
            except Method_Db.DoesNotExist:
                raise ValueError(f"Method_Db with ID {self.id} does not exist.")
        else:
            method_instance = None

        try:
            if not self.path_ph:
                raise ValueError("No photos to save. self.path_ph is empty.")

            for path_photo in self.path_ph:
                with open(path_photo, 'rb') as f:
                    image = Images_Db()
                    image.image.save(os.path.basename(path_photo), File(f))
                    image.filename = image.file_name()
                    image.uploader = self.user
                    image.user_conf = None
                    image.leds_conf = None
                    image.camera_conf = None

                    if method_instance:
                        image.method = method_instance
                    image.save()

                    images.append(image)

                    
                    if os.path.exists(path_photo):
                        os.remove(path_photo)

            return images  

        except Exception as e:
            print(f"Error saving photo in DB: {str(e)}")
            raise e  


    def photo_correction(self):
        # Corrects the images bending, product of using a fisheye lens
        # Hardcoded values for HQPicamera
        self.path_ph = []
        for path_ph in self.path_photo:
            self.path_photo = path_ph
            fixed_image = FixDistortionImage(self.path_photo)
            self.path_photo = fixed_image.path_photo
            self.path_ph.append(self.path_photo) 

class FixDistortionImage:
    def __init__(self, path):
        self.path_photo = path
        self.img = cv2.imread(self.path_photo)
        
        if os.path.exists(f'{self.path_photo}'):
            remove(f'{self.path_photo}')
        self.correction_mtx = np.array(
            [[1967.921637060819, 0.0, 980.07213571975], [0.0, 1964.823317953312, 741.073015742526], [0.0, 0.0, 1.0]])

        self.correction_dist = np.array([[-0.4778321949564693, 0.2886513041769561, 0.0016895448886501186,
                                          0.0047619737564622905, -0.12895314122999252]])

        self.rotation_angle = 179.8

        # Undistort the image
        if self.img is not None:
            self.undistort()
        else:
            print("image is None")

    def undistort(self):
        # Using the fixed values mtx and dist, it straighten the image
        # and also cut the black borders
        h, w = self.img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.correction_mtx,
                                                          self.correction_dist,
                                                          (w, h),
                                                          1,
                                                          (w, h))
        # undistort
        dst = cv2.undistort(self.img,
                            self.correction_mtx,
                            self.correction_dist,
                            None,
                            newcameramtx)
        # crop the image
        #x, y, w, h = roi
        y=150+10   #cropping 5 pixel, about 1 mm
        h=1150
        x=440-10   #cropping 5 pixel, about 1 mm
        w=1150
        dst = dst[y:y + h, x:x + w]
        self.path_photo = f'{os.path.splitext(self.path_photo)[0]}_{os.path.splitext(self.path_photo)[1]}'
        new_image = self.rotate_image(dst, self.rotation_angle)
        #crop_img = new_image[40:1190, 310:1490]

        cv2.imwrite(self.path_photo, new_image)           

    def rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
