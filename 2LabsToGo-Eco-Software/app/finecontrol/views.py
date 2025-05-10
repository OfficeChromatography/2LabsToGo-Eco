from connection.forms import OC_LAB
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from .forms import *
from .models import *

from django.http import HttpResponse
import csv

from finecontrol.calculations.volumeToZMovement import volume_to_z_movement
from finecontrol.gcode.GcodeGenerator import GcodeGenerator, GcodeGeneratorSP

from django.views.generic import FormView, View, DeleteView
from django.http import JsonResponse
from django.forms.models import model_to_dict

from sampleapp.models import *
from development.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http import Http404
from .serializers import AirSensorSerializer
import os


CLEANINGPROCESS_INITIALS = {'start_frequency': 100, 'stop_frequency': 500,
                            'steps': 50,'warmup_pressure': 20, 'times': 1}


form = {}


class MethodList(FormView):

    def get(self, request):
        """Returns a list with all the Methods saved in DB"""
        method = Method_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = []
        for i in method:
            icons = [1, 1, 1, 1]
            if not SampleApplication_Db.objects.filter(method=i):
                icons[0] = 0.3
                
            if not Development_Db.objects.filter(method=i):
                icons[1] = 0.3
                
            band_c = BandsComponents_Db.objects.filter(sample_application__method=i)
            
            if band_c.exists():
                for obj in band_c:
                    if obj.sample is None:
                        icons[3] = 0 # [1,0.3,1,0]
               
            data_saved.append([i.filename, i.id, icons])

        return JsonResponse(data_saved, safe=False)

class MethodListSP(FormView):

    def get(self, request):
        """Returns a list with all the Methods saved in DB"""
        method = Method_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = []
        for i in method:
            icons = [1, 1, 1, 1]
            if not SampleApplication_Db.objects.filter(method=i):
                icons[0] = 0.3
                
            if not Development_Db.objects.filter(method=i):
                icons[1] = 0.3
            band_c = BandsComponents_Db.objects.filter(sample_application__method=i)
            
            if band_c.exists():
                for obj in band_c:
                    if obj.sample is None:
                        icons[3] = 0 # [1,0.3,1,0]
            
            data_saved.append([i.filename, i.id, icons])
        return JsonResponse(data_saved, safe=False)


class MethodDelete(DeleteView):

    def delete(self, request, *args, **kwargs):
        Method_Db.objects.filter(auth_id=request.user).get(id=kwargs.get('id')).delete()
        return JsonResponse({}, safe=False)


class OcLabControl(View):
    def post(self, request):
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message': 'OcLab Paused!'})
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message': 'OcLab Stopped!'})
        if 'RESUME' in request.POST:
            OC_LAB.resume()
            return JsonResponse({'message': 'OcLab Resumed!'})
        if 'SEND' in request.POST:
            OC_LAB.send(request.POST['message'])
            return JsonResponse({'message': f'OcLab {request.POST["message"]} send !'})
        if 'SEND_NOW' in request.POST:
            OC_LAB.send_now(request.POST['message'])
            return JsonResponse({'message': f'OcLab {request.POST["message"]} fast send !'})
        if 'RESET' in request.POST:
            OC_LAB.reset()
            return JsonResponse({'message': f'OcLab {request.POST["message"]} reset !'})


class SyringeLoad(View):
    # def post:
    def get(self, request):
        if "LISTLOAD" in request.GET:
            syringe_load_db = SyringeLoad_Db.objects.filter(
                author=request.user).order_by('volume')
            volumes = [i.volume for i in syringe_load_db]
            return JsonResponse(volumes, safe=False)

    def post(self, request):
        # Creates a new vol in the database
        if 'SAVEMOVEMOTOR' in request.POST:
            try:
                SyringeLoad_Db.objects.filter(
                    volume=request.POST['SAVEMOVEMOTOR']).filter(
                    author=request.user)[0]
                return JsonResponse("Volume already exist!", safe=False)
            except IndexError:
                syringe_load = SyringeLoad_Db.objects.create(
                    volume=request.POST['SAVEMOVEMOTOR'], author=request.user)
                syringe_load.save()
                return JsonResponse("Volume saved!", safe=False)

        if 'DELETE' in request.POST:
            try:
                SyringeLoad_Db.objects.filter(
                    volume=request.POST['DELETE']).filter(author=request.user)[
                    0].delete()
                return JsonResponse("Volume Deleted!", safe=False)
            except IndexError:
                return JsonResponse("Volume doesn't exist!", safe=False)
        
        if 'MOVEMOTOR' in request.POST:
            syringe_type_volume = request.session.get('volume_type')
            syringe_type_length = request.session.get('length_type')
            
            if syringe_type_volume is None or syringe_type_length is None:
                return JsonResponse("Syringe settings are not available", safe=False, status=400)

            zMov = volume_to_z_movement(float(request.POST['MOVEMOTOR']), False, syringe_type_length, syringe_type_volume)
            if zMov > 45:
                message = "Volume set is too high"
                return JsonResponse(message, safe=False, status=400)
            mm_movement = round(300 - zMov, 2)
            OC_LAB.send(f"G0Z{mm_movement}")
            return JsonResponse("Volume save", safe=False)    

class SyringeType(View):
    
    def get(self, request):
        form = SyringeSettingsForm()
        syringe_type_volume = request.session.get('volume_type')
        syringe_type_length = request.session.get('length_type')
        
        return render(request, 'modules/syringetype/syringetype.html', {'form': form})
    
    def post(self, request):
        form = SyringeSettingsForm(request.POST)
        if form.is_valid():
            syringe_type_volume = form.cleaned_data.get('volume_type')
            syringe_type_length = form.cleaned_data.get('length_type')

            request.session['volume_type'] = syringe_type_volume
            request.session['length_type'] = syringe_type_length
            
        return render(request, 'modules/syringetype/syringetype.html', {'form': form})       

class Cleaning(object):

    def __init__(self):
        self.time_window = 1  # Minimun time for each frequency 5 sec
        self.duration = 0
        self.lines_left = 0

    def dinamic_cleaning(self, fi, fo, step, warmup_pressure): 
        # THE GCODE TO OPEN THE VALVE AT A CERTAIN frequency
        
        self.duration = 0
        dinamic_clean = []
        
        for j in range(1, step + 1):
            dinamic_clean.append(f'G98 F{fi}' + '\n')
            if j % 1 == 0:
                dinamic_clean.append(f'G97 P{warmup_pressure}\n')
            self.lines_left += 1
        self.duration += self.time_window
        return dinamic_clean
    
    def dinamic_rinsing(self, fi, fo, step): 
        # THE GCODE TO OPEN THE VALVE AT A CERTAIN frequency
        
        self.duration = 0
        dinamic_clean = []
        
        for j in range(1, step + 1):
            dinamic_clean.append(f'G98 F{fi}' + '\n')
            self.lines_left += 1
        self.duration += self.time_window
        return dinamic_clean

    def static_cleaning(self, volume, speed, syringe_type_length, syringe_type_volume):
        # Gcode to move the Pump for a specific volume from 0-position
        
        generate = GcodeGeneratorSP(True)
        zMovement = volume_to_z_movement(volume, True, syringe_type_length, syringe_type_volume)
        speed = round(speed * 60, 2)
        generate.set_position_x(5)
        generate.homming("Y")
        generate.set_relative()
        generate.open_valve()
        generate.linear_move_z(zMovement, speed)
        generate.wait_ms(500)
        generate.close_valve()
        generate.set_absolute()
        return generate.list_of_gcodes
    
    def static_rinsing(self, times, frequency):
        # Gcode to move the Pump for a specific volume from 0-position
    
        generate = GcodeGenerator(True)
        generate.static_cleaning(times, frequency)
        return generate.list_of_gcodes

    def warmup(self, times, frequency):
        # Gcode to move the Pump for a specific volume from 0-position
        
        generate = GcodeGenerator(True)
        generate.warmup_window(times, frequency)
        return generate.list_of_gcodes

clean = Cleaning()


class MotorControl(View):
    
    def get(self, request):
        return render(request, "./motorcontrol.html", form)


class Clean(View):
    CLEANINGPROCESS_INITIALS = {'start_frequency': 100, 'stop_frequency': 500,
                                'steps': 50, 'warmup_pressure': 1, 'times': 1}

    def get(self, request):
        OC_LAB.send('G0X1')
        form['CleaningProcessForm'] = CleaningProcessForm(
            initial=CLEANINGPROCESS_INITIALS)
        return render(request, "./cleanprocess.html", form)

    def post(self, request):
        if 'cycles' in request.POST:
            for i in range(0, int(request.POST['cycles'])):
                OC_LAB.send('M42 P63 T')
        return render(request, "./cleanprocess.html", {**form})

class CleanAS(View):
    CLEANINGPROCESS_INITIALS = {'start_frequency': 100, 'stop_frequency': 500,
                                'steps': 50, 'warmup_pressure': 1, 'times': 1}

    def get(self, request):
        OC_LAB.send('G0X1')
        form['CleaningProcessForm'] = CleaningProcessForm(
            initial=CLEANINGPROCESS_INITIALS)
        return render(request, "./cleanprocessas.html", form)

    def post(self, request):
        if 'cycles' in request.POST:
            for i in range(0, int(request.POST['cycles'])):
                OC_LAB.send('M42 P63 T')
        return render(request, "./cleanprocessas.html", {**form})

clean = Cleaning()

class StaticPurge(View):
    def post(self, request):
        rinse_volume = request.POST.get('rinse_volume')
        rinse_speed = request.POST.get('rinse_speed')
        syringe_type_volume = request.session.get('volume_type')
        syringe_type_length = request.session.get('length_type')
        if rinse_volume and rinse_speed:
            gcode = clean.static_cleaning(
                    float(rinse_volume),
                    float(rinse_speed),
                    int(syringe_type_length),
                    int(syringe_type_volume)
                )
            
            OC_LAB.print_from_list(gcode)
            
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        return JsonResponse({'message': 'ok'})

class StaticPurgeAS(View):
    def post(self, request):
        if request.POST.get('rinse_times'):
            gcode = clean.static_rinsing(
                int(request.POST.get('rinse_times')),
                int(request.POST.get('rinse_frequency')))
            OC_LAB.print_from_list(gcode)
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        return JsonResponse({'message': 'ok'})

class WarmUp(View):
    def post(self, request):
        if request.POST.get('warmup_times'):
            gcode = clean.warmup(
                int(request.POST.get('warmup_times')),
                int(request.POST.get('warmup_frequency')))
            OC_LAB.print_from_list(gcode)
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        return JsonResponse({'message': 'ok'})
    
class CleanControl(View):
    def post(self, request):
        if 'PROCESS' in request.POST:
            clean_param = CleaningProcessForm(request.POST)

            if clean_param.is_valid():
                clean_param = clean_param.cleaned_data
                gcode = clean.dinamic_cleaning(clean_param['start_frequency'],
                                               clean_param['warmup_pressure'],
                                               clean_param['steps'],
                                               clean_param['warmup_pressure'])

                OC_LAB.print_from_list(gcode)

                data = {
                    'message': f'Cleaning process in progress, please wait! \n'}
                data.update({'duration': clean.duration})
            else:
                data = {'message': 'ERROR'}
            return JsonResponse(data)

        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message': 'stopped'})
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message': 'paused'})

    def get(self, request):
        # Check the status
        if 'checkstatus' in request.GET:
            data = {'busy': 'true', 'message': '', }
            if OC_LAB.printing:
                data[
                    'message'] = f'Cleaning process in progress, please wait! \n'
                return JsonResponse(data)
            else:
                data['busy'] = 'false'
                data['message'] = 'Done!'
                return JsonResponse(data)

class CleanControlAS(View):
    def post(self, request):
        if 'PROCESS' in request.POST:
            clean_param = CleaningProcessForm(request.POST)

            if clean_param.is_valid():
                clean_param = clean_param.cleaned_data
                gcode = clean.dinamic_cleaning(clean_param['start_frequency'],
                                               clean_param['warmup_pressure'],
                                               clean_param['steps'],
                                               clean_param['warmup_pressure'])

                OC_LAB.print_from_list(gcode)

                data = {
                    'message': f'Cleaning process in progress, please wait! \n'}
                data.update({'duration': clean.duration})
            else:
                data = {'message': 'ERROR'}
            return JsonResponse(data)

        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'message': 'stopped'})
        if 'PAUSE' in request.POST:
            OC_LAB.pause()
            return JsonResponse({'message': 'paused'})

    def get(self, request):
        # Check the status
        if 'checkstatus' in request.GET:
            data = {'busy': 'true', 'message': '', }
            if OC_LAB.printing:
                data[
                    'message'] = f'Cleaning process in progress, please wait! \n'
                return JsonResponse(data)
            else:
                data['busy'] = 'false'
                data['message'] = 'Done!'
                return JsonResponse(data)

class GcodeEditor(View):

    def get(self, request):
        form['list_load'] = GcodeFile.objects.filter(
            uploader=request.user).order_by('-id')

        # LIST LOADING
        if 'LISTLOAD' in request.GET:
            gcodefiles = GcodeFile.objects.filter(
                uploader=request.user).order_by('-id')
            names = [i.filename for i in gcodefiles]
            return JsonResponse(names, safe=False)

        # FILE LOADING
        if 'LOADFILE' in request.GET:
            filename = request.GET.get('filename')
            gcodefile = GcodeFile.objects.filter(uploader=request.user,
                                                 filename=filename)

            # Open the file
            with open(str(gcodefile[0].gcode), 'r') as f:
                text = f.read()

            response = {'text': text, 'filename': gcodefile[0].filename,
                        'success': 'File opened!'}
            return JsonResponse(response)

        return render(request, "./gcodeeditor.html", form)

    def post(self, request):
        if 'UPLOAD' in request.POST:
            if request.FILES['file']:
                uploaded_file = request.FILES['file']

                if GcodeFile.objects.filter(filename=uploaded_file,
                                            uploader=request.user):
                    return JsonResponse(
                        {'danger': 'Filename already exist, change it!'})

                if 'gcode' in uploaded_file.content_type:
                    fs = FileSystemStorage('media/gfiles/')
                    new_name = fs.save(uploaded_file.name, uploaded_file)

                    gcode = GcodeFile()
                    gcode.filename = uploaded_file.name
                    gcode.gcode = fs.location + '/' + new_name
                    gcode.gcode_url = fs.url(new_name)
                    gcode.uploader = request.user
                    gcode.save()
                    return JsonResponse({'success': 'File Saved!'})
                else:
                    return JsonResponse({'danger': 'Invalid File'})
            else:
                return JsonResponse({'danger': 'Please select a File'})

        # SAVE FILE
        if 'SAVE' in request.POST:

            filename = request.POST.get('name')
            text = request.POST.get('text')
            fs = FileSystemStorage('media/gfiles/')
            gcodefile = GcodeFile.objects.filter(uploader=request.user,
                                                 filename=filename)

            # if the file exist then edit
            if gcodefile:
                # Get relaitve path from app folder so that can be opened
                path_rel = os.path.relpath(str(gcodefile[0].gcode), '/app/')
                with open(path_rel, 'w+') as f:
                    myfile = File(f)
                    myfile.write(text)
                    new_name = fs.save(filename + '.gcode', content=myfile)
                return JsonResponse({'info': f'{filename} edited'})

            # Create the file
            with open(f'last.gcode', 'w+') as f:
                myfile = File(f)
                myfile.write(text)
                new_name = fs.save(filename + '.gcode', content=myfile)

                gcode = GcodeFile()
                gcode.filename = filename
                gcode.gcode = fs.location + '/' + new_name
                gcode.gcode_url = fs.url(new_name)
                gcode.uploader = request.user
                gcode.save()
                return JsonResponse({'success': 'File Saved!'})

        # REMOVE FILE
        if 'REMOVE' in request.POST:
            filename = request.POST.get('name')
            if not filename:
                return JsonResponse({'warning': 'Choose a file!'})

            try:
                file = GcodeFile.objects.get(filename=filename,
                                             uploader=request.user)
                file.delete()
            except:
                return JsonResponse({'warning': 'Something went wrong!'})

            return JsonResponse({'success': 'File removed!'})

        # RUN FILE
        if 'START' in request.POST:
            filename = request.POST.get('name')
            if not filename:
                return JsonResponse(
                    {'warning': 'First save the file and Open it!'})
            try:
                file = GcodeFile.objects.get(filename=filename,
                                             uploader=request.user)
                if file:
                    with open(f'{file.gcode}', 'r') as f:
                        OC_LAB.print_from_file(f)
                        return JsonResponse({'success': 'Printing!'})
            except DoesNotExist:
                return JsonResponse({'danger': 'File Not Found'})

        # STOP FILE
        if 'STOP' in request.POST:
            OC_LAB.cancelprint()
            return JsonResponse({'danger': 'STOP'})

class DryPump(View):
    def get(self,request):
        return render(request, "./drypump.html", form)

class DryPumpControl(View):
    def post(self, request):
        
        generate = GcodeGenerator(True)
        active = request.POST.get('active')
        if (active =='On'):
            generate.drypump(request.POST.get('times'))
        elif (active =='Off'):
            OC_LAB.send('Test')
        OC_LAB.print_from_list
        return JsonResponse({'message': 'ok'})
    def get (self, request):
        return JsonResponse({'message': 'ok'})
        
class WayValve(View):
    def get(self,request):
        return render(request, "./wayvalve.html", form)

#class WayValveControl(View):
#    def post(self, request):
#        
#        generate = GcodeGenerator(True)
#        active = request.POST.get('active')
#        if (active =='On'):
#            generate.wayvalve(request.POST.get('times'))
#        elif (active =='Off'):
#            OC_LAB.send('Test')
#        OC_LAB.print_from_list
#        return JsonResponse({'message': 'ok'})
#    def get (self, request):
#        return JsonResponse({'message': 'ok'})

class DispValve(View):
    def get(self,request):
        return render(request, "./dispensevalve.html", form)

class Temperature(View):
    # Manage the GET request
    def get(self, request):
        OC_LAB.send('M42I1P23S0')
        return render(request, "./temperature.html", form)


class TempControl(View):
    def post(self, request):
        
        generate = GcodeGenerator(True)
        active = request.POST.get('active')
        if (active == 'On'):
            generate.hold_bed_temperature(request.POST.get('temp'))
            generate.report_bed_temperature(4)
        elif (active == 'Off'):
            generate.hold_bed_temperature(0)
            generate.report_bed_temperature(0)
        OC_LAB.print_from_list(generate.list_of_gcodes)
        return JsonResponse({'message': 'ok'})

    def get(self, request):
        return JsonResponse({'message': 'ok'})

class Cells(View):
    # Mange the GET request
    def get(self,request):
        return render(request, "./cells.html", form)

class IncubationControl(View):
    def post(self, request):
        OC_LAB.send('M42I1P24')
        generate = GcodeGenerator(True)
        active = request.POST.get('active')
        if (active == 'On'):
            generate.hold_incubation_temperature(request.POST.get('temp'))
        elif (active == 'Off'):
            generate.hold_incubation_temperature(0)
        OC_LAB.print_from_list(generate.list_of_gcodes)
        return JsonResponse({'message': 'ok'})

class Incubation(View):
    # Mange the GET request
    def get(self,request):
        return render(request, "./incubation.html", form)

class Light(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./lightcontrol.html", form)
    
class UVLed_Light_265(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./uv265lightcontrol.html", form)

class UVLed_Light_365(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./uv365lightcontrol.html", form)

class Neo_Light(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./neolightcontrol.html", form)

class Back_Light(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./backlightcontrol.html", form)
    
class Fan(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./fancontrol.html", form)

class Humidity(View):
    # Manage the GET request
    def get(self, request):
        return render(request, "./humiditycontrol.html", form)

class AirSensorList(APIView):
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        measure = AirSensor_Db.objects.all()
        measures = AirSensorSerializer(measure, many=True)
        return Response(measures.data)

    def post(self, request, format=None):
        serializer = AirSensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AirSensorDetail(APIView):
    parser_classes = [JSONParser]

    def get_object(self, pk):
        try:
            return AirSensor_Db.objects.get(pk=pk)
        except AirSensor_Db.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        measure = self.get_object(pk)
        serializer = AirSensorSerializer(measure)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        measure = self.get_object(pk)
        serializer = AirSensorSerializer(measure, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Export(View):

    def append_method_to_csv(self, writer, method):
        header = self.header(method.keys())
        writer.writerow(header)
        writer.writerow(method.values())

    def get(self, request, id):
        c = ExportToCsv(id)
        return c.response


class ExportToCsv:

    def __init__(self, id):
        self.method = Method_Db.objects.get(pk=id)
        self.response = HttpResponse(content_type='text/csv')
        self.response[
            'Content-Disposition'] = "attachment; filename=" + f"{self.method.filename}.csv"
        self.writer = csv.writer(self.response)

        try:
            self.sample_application = {"data": {},
                                       "object": SampleApplication_Db.objects.get(
                                           method=self.method)}
            self.sample_app_2_csv()
        except:
            pass

        try:
            self.development = {"data": {},
                                "object": Development_Db.objects.get(
                                    method=self.method)}
            self.development_2_csv()
        except:
            pass

    def header(self, listOfNames):
        return [str(i).upper() for i in listOfNames]

    def space_methods(self):
        self.space(5)

    def space(self, n):
        for i in range(0, n):
            self.writer.writerow([])

    def append_method_to_csv(self, method):
        header = self.header(method.keys())
        self.writer.writerow(header)
        self.writer.writerow(method.values())

    def object_to_dictionary(self, dict_data, obj, attrs):

        if isinstance(obj, Images_Db):
            for attr in attrs:
                sub = getattr(obj, attr)
                fields = getattr(getattr(sub, "_meta"), 'fields')
                dict_data.update(
                    model_to_dict(sub, fields=[field.name for field in fields]))
        else:
            for attr in attrs:
                try:
                    dict_data.update(model_to_dict(getattr(obj, attr).get(),
                                                   exclude=["id", ]))
                except:
                    pass

    def sample_app_2_csv(self):
        self.object_to_dictionary(self.sample_application['data'],
                                  self.sample_application['object'],
                                  ["pressure_settings", "plate_properties",
                                   "band_settings", "zero_properties",
                                   "movement_settings"])
        self.writer.writerow(["SAMPLE APPLICATION", ])
        bands_components = BandsComponents_Db.objects.filter(
            sample_application=self.sample_application['object']).values()
        self.append_method_to_csv(self.sample_application['data'])
        self.writer.writerow(["BAND COMPONENTS", ])
        for band_component in bands_components:
            self.append_method_to_csv(band_component)
        self.space_methods()

    def development_2_csv(self):
        self.object_to_dictionary(self.development['data'],
                                  self.development['object'],
                                  ["pressure_settings", "plate_properties",
                                   "band_settings", "zero_properties"])

        self.writer.writerow(["DEVELOPMENT", ])
        self.append_method_to_csv(self.development['data'])

        flows = Flowrate_Db.objects.filter(
            development=self.development['object']).values('value')
        self.writer.writerow(["FLOWRATES", ])
        for flowrate_entry in flows:
            self.append_method_to_csv(flowrate_entry)
        self.space_methods()
    

