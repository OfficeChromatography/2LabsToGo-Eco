from django.views.generic import FormView, View
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
import json

from finecontrol.calculations.development import calculateDevelopment
from finecontrol.forms import data_validations, data_validations_and_save, Method_Form
from finecontrol.models import Method_Db

from django.core.exceptions import ObjectDoesNotExist
import csv
import urllib.parse

class ImportDevelopmentCSV(View):
    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return JsonResponse({'error': 'No CSV file uploaded'}, status=400)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=',', quotechar='"')

            form_data = {}
            waiting_time_data = []
            is_waiting_time_section = False

            for row in reader:
                if len(row) < 2:
                    continue

                key = row[0].strip()
                value = row[1].strip()

                if key == 'Waiting Time Data':
                    is_waiting_time_section = True
                    continue

                if is_waiting_time_section:
                    application_index = key.split('_')[1]
                    waiting_time_data.append({
                        'application': application_index,
                        'waitingTime': value
                    })
                else:
                    if key in ['filename', 'description']:
                        form_data[key] = urllib.parse.unquote(value)
                    elif key == 'flowrate':
                        form_data[key] = json.loads(value.replace("'", "\""))
                    else:
                        form_data[key] = value

            request.session['imported_form_data'] = form_data
            request.session['imported_waiting_time_data'] = waiting_time_data

            return redirect('development')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class DevelopmentDelete(View):

    def delete(self, request, id):
        apps = Development_Db.objects.filter(method=Method_Db.objects.get(pk=id))
        Method_Db.objects.get(pk=id).delete()
        apps.delete()
        return JsonResponse({})


class DevelopmentView(FormView):
    def get(self, request):
        """Manage the HTML view in Development"""
        OC_LAB.send(f'M92Z1600')
        OC_LAB.send(f'M203Z5')  
        OC_LAB.send(f'M42P49S255')
        OC_LAB.send(f'M42P36S255')
        OC_LAB.send(f'G28YX')
        return render(request, 'development.html', {})


class DevelopmentDetail(View):
    
    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        method = Method_Db.objects.get(pk=id_object)

        if not Development_Db.objects.filter(method=method):
            response.update({"filename": getattr(method, "filename")})
            response.update({"id": id_object})
        else:
            dev_config = Development_Db.objects.get(method=method)
            response.update(model_to_dict(dev_config.pressure_settings.get(), exclude=["id", ]))
            response.update(model_to_dict(dev_config.plate_properties.get(), exclude=["id", ]))
            response.update(model_to_dict(dev_config.band_settings.get(), exclude=["id", ]))
            response.update(model_to_dict(dev_config.zero_properties.get(), exclude=["id", ]))
            response.update(model_to_dict(method))

            flowrate_entry = Flowrate_Db.objects.filter(development=dev_config.id).values('value')
            
            response.update({'flowrate': [entry for entry in flowrate_entry]})

        waiting_times_data = list(
            WaitTime_Db.objects.filter(development=dev_config).values('waitTime', 'application')
        )
        response.update({'waitingTimes': waiting_times_data})

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        try:
            id = request.POST.get("selected-element-id")
            flowrate = request.POST.get('flowrate')
            flowrate = json.loads(flowrate) if flowrate else []
            if not id or not Development_Db.objects.filter(method=Method_Db.objects.get(pk=id)):
                development_form = Development_Form(request.POST)
                if development_form.is_valid():
                    development_instance = development_form.save(commit=False)
                    development_instance.auth = request.user
                    method_form = Method_Form(request.POST)

                    if not id:
                        method = method_form.save(commit=False)
                        method.auth = request.user
                        method.save()
                    else:
                        method = Method_Db.objects.get(pk=id)
                    development_instance.method = method
                    development_instance.save()
                    objects_save = data_validations_and_save(
                        plate_properties=PlateProperties_Form(request.POST),
                        pressure_settings=PressureSettings_Form(request.POST),
                        zero_position=ZeroPosition_Form(request.POST),
                        band_settings=DevelopmentBandSettings_Form(request.POST),
                    )
                    development_instance.pressure_settings.add(objects_save["pressure_settings"])
                    development_instance.plate_properties.add(objects_save["plate_properties"])
                    development_instance.zero_properties.add(objects_save["zero_position"])
                    development_instance.band_settings.add(objects_save["band_settings"])
                else:
                    return HttpResponseBadRequest({"error": "Please check all the inputs!"})
            else:
                method = Method_Db.objects.get(pk=id)
                method_form = Method_Form(request.POST, instance=method)
                method_form.save()
                development_instance = Development_Db.objects.get(method=method)
                development_form = Development_Form(request.POST, instance=development_instance)
                dev_inst = development_form.save(commit=False)
                dev_inst.method = method
                dev_inst.save()
                data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST,
                                                        instance=development_instance.plate_properties.get()),
                    pressure_settings=PressureSettings_Form(request.POST,
                                                            instance=development_instance.pressure_settings.get()),
                    zero_position=ZeroPosition_Form(request.POST,
                                                    instance=development_instance.zero_properties.get()),
                    band_settings=DevelopmentBandSettings_Form(request.POST,
                                                            instance=development_instance.band_settings.get()),
                )
                development_instance.flowrates.all().delete()
            
            for flow_value in flowrate:
                flowrate_form = Flowrate_Form(flow_value)
                if flowrate_form.is_valid():
                    flowrate_object = flowrate_form.save()
                    development_instance.flowrates.add(flowrate_object)

            waiting_times_str = request.POST.get("waitingTimes")
            if waiting_times_str:
                try:
                    waiting_times = json.loads(waiting_times_str)
                except ValueError:
                    return JsonResponse({"error": "Formato JSON inválido en waitingTimes"}, status=400)

                
                WaitTime_Db.objects.filter(development=development_instance).delete()

                for wt in waiting_times:
                    application = wt.get("application")
                    waiting_time_value = wt.get("waitTime")
                    if application is not None and waiting_time_value is not None:
                        WaitTime_Db.objects.create(
                            development=development_instance,
                            waitTime=waiting_time_value,
                            application=application
                        )
                    else:
                        print("Error: Missing 'application' or 'waitTime' in:", wt)

            return JsonResponse({'message': 'Data saved successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class DevelopmentAppPlay(View):
    def post(self, request):
        try:
            method_id = request.POST.get('selected-element-id')
            
            waiting_times_request = []
            waiting_times_str = request.POST.get('waitingTimes')
            # Manejo de 'waitingTimes'
                       
            if waiting_times_str:
                try:
                    waiting_times_request = json.loads(waiting_times_str)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid format for waitingTimes.'}, status=400)
            else:
                return JsonResponse({'error': 'waitingTimes not provided.'}, status=400)

                if waiting_times_str:
                    waiting_times_request = json.loads(waiting_times_str)
            forms_data = data_validations(
                plate_properties=PlateProperties_Form(request.POST),
                pressure_settings=PressureSettings_Form(request.POST),
                zero_position=ZeroPosition_Form(request.POST),
                band_settings=DevelopmentBandSettings_Form(request.POST)
            )
            forms_data['waiting_times'] = waiting_times_request
            syringe_type_volume_str = request.POST.get('volume_type')
            syringe_type_length_str = request.POST.get('length_type')

            # Manejo de 'flowrate'
            flowrates_str = request.POST.get('flowrate')
            if flowrates_str:
                try:
                    flowrates = json.loads(flowrates_str)
                    if not isinstance(flowrates, list) or len(flowrates) == 0:
                        return JsonResponse({'error': 'Invalid or empty flowrate list.'}, status=400)
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid format for flowrate.'}, status=400)
            else:
                return JsonResponse({'error': 'Flowrate not provided.'}, status=400)
            
            forms_data['flowrate'] = flowrates
            # flowrates = json.loads(request.POST.get('flowrate', '[]'))

            # if not flowrates:
            #     return JsonResponse({'error': 'No flowrates provided.'}, status=400)
            # forms_data['flowrate'] = flowrates

            # Validación básica
            if not syringe_type_volume_str or not syringe_type_length_str:
                return JsonResponse({'error': 'Syringe type not specified.'}, status=400)

            # Ejemplo: quitar el sufijo " mm" y convertir a float
            try:
                syringe_type_length_num = float(syringe_type_length_str.replace(' mm', ''))
                syringe_type_volume_num = float(syringe_type_volume_str)
            except ValueError:
                return JsonResponse({'error': 'Invalid syringe type format.'}, status=400)
            gcode = calculateDevelopment(forms_data, syringe_type_length_num, syringe_type_volume_num)
            OC_LAB.print_from_list(gcode)

            return JsonResponse({'message': 'Gcode generated successfully.'})

        except Development_Db.DoesNotExist:
            return JsonResponse({'error': 'Development object not found.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DevelopmentWaitingTime(View):

    def get(self, request, id=None):
        if 'imported_data' in request.GET: 
            waiting_times = request.GET.get('waiting_times', [])
            return JsonResponse(waiting_times, safe=False)

        try:
            development_object = Development_Db.objects.get(method=id)
            query = WaitTime_Db.objects.filter(development=development_object).values('waitTime', 'application')
            response = list(query)
            if not response:
                return HttpResponseBadRequest({"data": "No Waiting times saved!"})
            return JsonResponse(response, safe=False)
        except Development_Db.DoesNotExist:
            return HttpResponseBadRequest({"data": "Development id not Found"})
        except Exception as e:
            return HttpResponseBadRequest({"data": str(e)})

    def post(self, request):
        try:
            if not request.body:
                return JsonResponse({"data": "Empty body in the request"}, status=400)

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"data": "Invalid JSON format"}, status=400)

            dev_id = data.get('development_id')
            waiting_times = data.get('waitingTimes', [])

            if not dev_id:
                return JsonResponse({"data": "No se guardaron datos en la base de datos porque no se proporcionó `development_id`"}, status=400)

            if not waiting_times:
                return JsonResponse({"data": "No waiting times provided"}, status=400)

            development_object = Development_Db.objects.get(method=dev_id)

            WaitTime_Db.objects.filter(development=development_object).delete()

            for wt in waiting_times:
                WaitTime_Db.objects.create(
                    development=development_object,
                    waitTime=wt.get('waitingTime'),
                    application=wt.get('application')
                )

            return JsonResponse({"data": f"Data Saved in development_object {dev_id}"})

        except Development_Db.DoesNotExist:
            return JsonResponse({"data": "Development object not found"}, status=400)
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)

class DevelopmentViewWaitingTimes(View):

    def get(self, request):
        return render(request, 'modules/development/waitingtime/table/table.html', {})
