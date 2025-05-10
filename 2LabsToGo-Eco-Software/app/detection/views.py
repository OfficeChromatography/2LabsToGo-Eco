from django.views.generic import FormView, View
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from connection.forms import OC_LAB
from app.settings import STATIC_ROOT, MEDIA_ROOT
from .models import *
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
import cv2
import numpy as np
from  django.http import QueryDict
import json

from django.core.files import File
import re
from .takeimage import *
from django.core.exceptions import ObjectDoesNotExist
import os
from finecontrol.forms import data_validations, data_validations_and_save
import csv
import urllib.parse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from django.conf import settings
from django.views import View
from PIL import Image
MOTION_MODEL = ((0, 'Translation'),
                    (1, 'Euclidean'),
                    (2, 'Affine'),
                    (3, 'Homography'))

class ImportCSV(View):
    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return JsonResponse({'error': 'No CSV file uploaded'}, status=400)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=',', quotechar='"')

            form_data = {}
            color_selected = {}  
            default_image_url = 'http://127.0.0.1:8000/static/img/login.jpg'

            for row in reader:
                if len(row) < 2:
                    continue  

                key = row[0].strip()  
                value = row[1].strip()
                if key in ['filename', 'note']:
                    form_data[key] = urllib.parse.unquote(value)
                elif key == 'colour_gains':
                    form_data[key] = urllib.parse.unquote(value).replace('%2C', ',')
                elif key == 'image_id':
                    form_data['image_id'] = default_image_url
                else:
                    form_data[key] = value
            form_data['image_id'] = default_image_url

            request.session['imported_form_data'] = form_data
            request.session['imported_color_selected'] = color_selected

            return redirect('capture')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class Image_Process(View):
    
    def get(self, request):
            last_photo = Images_Db.objects.latest('id')
            photo_path = last_photo.image.url
            full_photo_url = request.build_absolute_uri(photo_path)
            context = {
                'imagepath': full_photo_url,
            }   
            return render(request, 'Image_Process.html', context) 
        
    def post(self, request):
        
        direction = request.POST.get('direction')
        photo_name = request.POST.get("current_photo_id")

        if direction == 'next' :
            current_photo = Images_Db.objects.get(image__contains=photo_name)
            current_photo_id = int(current_photo.id)
            next_photo_id = current_photo_id + 1
            next_photo = Images_Db.objects.get(id=next_photo_id)
            if next_photo:
                
                photo_path = next_photo.image.url
                full_photo_url = request.build_absolute_uri(photo_path)

        elif direction == 'pre':
                current_photo = Images_Db.objects.get(image__contains=photo_name)
                current_photo_id = int(current_photo.id)
                previous_photo_id = current_photo_id - 1
                previous_photo = Images_Db.objects.get(id=previous_photo_id)
                if previous_photo:
                    photo_path = previous_photo.image.url
                    full_photo_url = request.build_absolute_uri(photo_path)
        else:
            last_photo = Images_Db.objects.latest('id')
            photo_path = last_photo.image.url
            full_photo_url = request.build_absolute_uri(photo_path)
    
        return JsonResponse({'imagepath':full_photo_url})
        

            
class WhiteBalance(View):
    def post(self, request):
        if 'image' not in request.FILES:
            return JsonResponse({"error": "No image file provided"}, status=400)
        
        image_file = request.FILES['image']

        try:
            img = Image.open(image_file).convert('RGB')
            img = np.array(img)
            
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            wb = cv2.xphoto.createSimpleWB()
            img_balanced = wb.balanceWhite(img_bgr)
            
            img_rgb = cv2.cvtColor(img_balanced, cv2.COLOR_BGR2RGB)

            image_io = BytesIO()
            Image.fromarray(img_rgb).save(image_io, format='PNG')
            image_io.seek(0)  

            return HttpResponse(image_io, content_type='image/png')

        except Exception as e:
            print(f"Error in WhiteBalance View: {str(e)}")
            return JsonResponse({"error": f"Processing failed: {str(e)}"}, status=500)
 
class DetectionView(FormView):
    def get(self, request):
        form = {}
        initial = basic_conf()
        imported_data = request.session.pop('imported_form_data', None)
        color_selected = request.session.pop('imported_color_selected', None)

        if imported_data:
              
            initial.update(imported_data)

        form['FormatControlsForm'] = ShootConfigurationForm(initial=initial)
        form['CameraControlsForm'] = CameraControlsForm(initial=initial)
        form['UserControlsForm'] = UserControlsForm(initial=initial)
        form['LedsControlsForm'] = LedsControlsForm(initial=initial)
        
        image_info = {'url': 'http://127.0.0.1:8000/static/img/login.jpg'}
        if 'image_id' in initial:
            image_id = initial['image_id']
            if image_id.startswith('http'):
                image_info = {'url': image_id}
            else:
                image_info = {'url': f'http://127.0.0.1:8000/capture/load/{image_id}/'}
        context = {**form, **image_info}

        if color_selected:
            context['color_selected'] = color_selected
            context['importedColorSelected'] = json.dumps(color_selected)

        if imported_data:
            context['importedFormData'] = json.dumps(imported_data)

        return render(request, 'capture.html', context)

class TakeImage(View):
    def post(self, request):
        try:
            action = request.POST.get('action', 'TAKE_PHOTO')
            image_id = request.POST.get("image_id")

            if action == "SAVE_NOTE":
                image_id = request.POST.get('id')
                note_text = request.POST.get('note')
                print(f"Saving note for image ID {image_id}: {note_text}")

                try:
                    image_instance = Images_Db.objects.get(id=image_id)
                    image_instance.note = note_text
                    image_instance.save()
                    return JsonResponse({'message': 'Note saved successfully!'}, status=200)
                except Images_Db.DoesNotExist:
                    print(f"Image with ID {image_id} not found.")
                    return JsonResponse({'error': 'Image not found'}, status=404)

            elif action == "TAKE_PHOTO":
                color_selected = request.POST.getlist('colorSelected[]')
                method_selected = request.POST.getlist('methodSelected[]')

                if len(color_selected) != 3:
                    print("Invalid colorSelected data:", color_selected)
                    return JsonResponse({'error': 'Invalid colorSelected data'}, status=400)
                if len(method_selected) != 2:
                    print("Invalid methodSelected data:", method_selected)
                    return JsonResponse({'error': 'Invalid methodSelected data'}, status=400)

                
                try:
                    color_dict = {
                        "red": int(color_selected[0]),
                        "green": int(color_selected[1]),
                        "blue": int(color_selected[2]),
                    }
                except ValueError as ve:
                    print("Error parsing color values:", ve)
                    return JsonResponse({'error': 'Invalid color values'}, status=400)

                try:
                    print("Starting photo shoot process...")
                    photo_shoot = PhotoShootManager(request)
                    photo_shoot.set_camera_configurations(color_dict)
                    photo_shoot.shoot()
                    photo_shoot.photo_correction()

                    image_id = request.POST.get("image_id")
                    if image_id:
                        try:
                            phantom_image = Images_Db.objects.get(id=image_id)
                        except Images_Db.DoesNotExist:
                            phantom_image = None
                    else:
                        phantom_image = None

                    images = photo_shoot.save_photo_in_db()

                    photo_urls = []
                    photo_ids = []
                    for photo_object in images:
                        user_conf = camera_conf = leds_conf = None

                        if phantom_image:
                            if phantom_image.user_conf:
                                if not photo_object.user_conf:
                                    old_conf = phantom_image.user_conf
                                    conf_dict = model_to_dict(old_conf)
                                    conf_dict.pop('id', None)
                                    user_conf = UserControls_Db.objects.create(**conf_dict)
                                    photo_object.user_conf = user_conf
                                else:
                                    user_conf = photo_object.user_conf

                            if phantom_image.camera_conf:
                                if not photo_object.camera_conf:
                                    old_conf = phantom_image.camera_conf
                                    conf_dict = model_to_dict(old_conf)
                                    conf_dict.pop('id', None)
                                    camera_conf = CameraControls_Db.objects.create(**conf_dict)
                                    photo_object.camera_conf = camera_conf
                                else:
                                    camera_conf = photo_object.camera_conf

                            if phantom_image.leds_conf:
                                if not photo_object.leds_conf:
                                    old_conf = phantom_image.leds_conf
                                    conf_dict = model_to_dict(old_conf)
                                    conf_dict.pop('id', None)
                                    leds_conf = Leds_Db.objects.create(**conf_dict)
                                    photo_object.leds_conf = leds_conf
                                else:
                                    leds_conf = photo_object.leds_conf

                            photo_object.note = phantom_image.note

                        photo_object.save()
                        
                        url = request.META['HTTP_ORIGIN'] + photo_object.image.url
                        photo_urls.append(url)
                        photo_ids.append(photo_object.id)

                    leds_data   = model_to_dict(leds_conf)   if leds_conf else {}
                    camera_data = model_to_dict(camera_conf) if camera_conf else {}
                    user_data   = model_to_dict(user_conf)   if user_conf else {}
                    response_images = []
                    for i, url in enumerate(photo_urls):
                        response_images.append({
                            "image_id": photo_ids[i],
                            "url": url,
                            "note": phantom_image.note if phantom_image else "",
                            "user_conf": model_to_dict(user_conf) if user_conf else {},
                            "leds_conf": model_to_dict(leds_conf) if leds_conf else {},
                            "camera_conf": model_to_dict(camera_conf) if camera_conf else {},
                        })

                    return JsonResponse({
                        "images": response_images,
                        "image_id": photo_ids[-1] 
                    })


                except Exception as e:
                    print("Error during photo shoot process:", str(e))
                    return JsonResponse({'error': str(e)}, status=500)

            else:
                print("Invalid action:", action)
                return JsonResponse({'error': 'Invalid action'}, status=400)

        except Exception as e:
            print("Unexpected error occurred:", str(e))
            return JsonResponse({'error': 'An error occurred on the server. Check logs for details.'}, status=500)

class DetectionDetail(View):
    def get(self, request, id):
        """Loads a method and its associated images with configurations"""
        try:
            method = Method_Db.objects.get(id=id, auth=request.user)
        except Method_Db.DoesNotExist:
            return JsonResponse({"error": "No existe ese método"}, status=404)

        images = Images_Db.objects.filter(method=method).order_by("id")

        response_images = []
        for img in images:
            response_images.append({
                "image_id": img.id,
                "url": img.image.url if img.image else "/media/default.jpg",
                "note": img.note or "",
                "user_conf": model_to_dict(img.user_conf) if img.user_conf else {},
                "leds_conf": model_to_dict(img.leds_conf) if img.leds_conf else {},
                "camera_conf": model_to_dict(img.camera_conf) if img.camera_conf else {},
            })

        return JsonResponse({
            "filename": method.filename,
            "id": method.id,
            "images": response_images
        })
   
    def post(self, request):
        method_id = request.POST.get("selected-element-id")

        if method_id:
            method = Method_Db.objects.get(pk=method_id)
            method_form = Method_Form(request.POST, instance=method)
            if method_form.is_valid():
                method_form.save()
            else:
                return JsonResponse({"errors": method_form.errors}, status=400)
        else:
            temp_method = Method_Form(request.POST)
            if temp_method.is_valid():
                method = temp_method.save(commit=False)
                method.auth = request.user
                method.save()
            else:
                return JsonResponse({"errors": temp_method.errors}, status=400)
        new_image = Images_Db.objects.create(
            method=method,
            filename="placeholder_no_photo",   
            uploader=request.user,
            note=request.POST.get("note", "New image"),
        )

        camera_form = CameraControlsForm(request.POST)
        user_form   = UserControlsForm(request.POST)
        leds_form   = LedsControlsForm(request.POST)

        if not (camera_form.is_valid() and user_form.is_valid() and leds_form.is_valid()):
            errors = {
                "camera_errors": camera_form.errors,
                "user_errors": user_form.errors,
                "leds_errors": leds_form.errors,
            }
            return JsonResponse({"errors": errors}, status=400)

        camera_instance = camera_form.save(commit=False)
        camera_instance.pk = None
        camera_instance.save()

        user_instance = user_form.save(commit=False)
        user_instance.pk = None
        user_instance.save()

        leds_instance = leds_form.save(commit=False)
        leds_instance.pk = None
        leds_instance.save()

        new_image.camera_conf = camera_instance
        new_image.user_conf   = user_instance
        new_image.leds_conf   = leds_instance
        new_image.save()
        images = Images_Db.objects.filter(method=method).order_by("id")

        response_images = []
        for img in images:
            response_images.append({
                "image_id": img.id,
                "url": img.image.url if img.image else "/media/default.jpg",
                "note": img.note or "",
                "user_conf": model_to_dict(img.user_conf) if img.user_conf else {},
                "leds_conf": model_to_dict(img.leds_conf) if img.leds_conf else {},
                "camera_conf": model_to_dict(img.camera_conf) if img.camera_conf else {},
            })

        return JsonResponse({
            "filename": method.filename,
            "id": method.id,
            "images": response_images
        })
        
        
class GetConfig(View):
    def get(self, request, id):
        image = Images_Db.objects.get(pk=id)
        response = {}
        user_conf = model_to_dict(image.user_conf,
                                fields=[field.name for field in image.user_conf._meta.fields])
        leds_conf = model_to_dict(image.leds_conf,
                                fields=[field.name for field in image.leds_conf._meta.fields])
        camera_conf = model_to_dict(image.camera_conf,
                                fields=[field.name for field in image.camera_conf._meta.fields])
        response.update({**{
                        'user_conf': user_conf,
                        'leds_conf': leds_conf,
                        'camera_conf': camera_conf,
                        'note': image.note,
                        }})
        return JsonResponse(response)

class DeleteImage(View):
    def delete(self, request, id):
        if not Images_Db.objects.get(pk=id):
            return JsonResponse({'warning': 'Something went wrong!'})
        else:
            image = Images_Db.objects.get(pk=id)
            path = os.path.join(MEDIA_ROOT, str(image.image))
            if os.path.exists(path):
                os.remove(path)
                image.delete()
            return JsonResponse({'success': 'File removed!'})

class DeleteImages(View):
    def delete(self, request, id):
        apps = Images_Db.objects.filter(method=Method_Db.objects.get(pk=id))
        Method_Db.objects.get(pk=id).delete()
        for image in apps:
            path = os.path.join(MEDIA_ROOT, str(image.image))
            if os.path.exists(path):
                os.remove(path)
        apps.delete()
        return JsonResponse({})
