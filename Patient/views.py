from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from . import forms
from .models import Bell

emergency_medical_need_list = ['sos', 'vaginal_bleed', 'baby', 'water-broke', 'pressure', 'pain', 'nausea',
                               'beeping', 'foley', 'help']
non_medical_need_list = ['bathroom', 'linens', 'food', 'settle']
question_list = ['nurse', 'health-care']
global room_number

messages = {'sos'           :["Need a nurse STAT",                               1, "RN",    "Y"],
            'water-broke'   :["I think my water broke",                          1, "RN",    "N"],
            'pain'          :["I am feeling a lot of pain",                      1, "RN",    "N"],
            'pressure'      :["I am feeling a lot of pressure/urge to push",     1, "RN",    "N"],
            'vaginal_bleed' :["I am having vaginal bleeding",                    1, "RN",    "Y"],
            'nausea'        :["I have some nausea",                              2, "RN",    "N"],
            'beeping'       :["Something is beeping in my room",                 2, "RN",    "N"],
            'foley'         :["My foley / Cervidil came out",                    2, "RN",    "N"],
            'bathroom'      :["I need help to the bathroom",                     2, "RN",    "N"],
            'linens'        :["I would like some linens",                        3, "HCA",   "N"],
            'food'          :["I would like some food or water",                 3, "RN",    "N"],
            'settle'        :["I need help getting settled into my room",        3, "HCA",   "N"],
            'nurse'         :["I have a non-urgent question",                    3, "RN",    "N"],
            'health-care'   :["I have a non-urgent question",                    3, "HCA",   "N"]
            }


def domain(request, *args, **kwargs):
    return render(request, "domain.html", {})


def get_room_number(request, *args, **kwargs):
    return render(request, "room_number.html", {})


def home_view(request, *args, **kwargs):
    global room_number
    room_number = request.POST.get("input_number")
    print(room_number)
    return render(request, "home.html", {"room_number": room_number})


def medical_need(request, *args, **kwargs):
    return render(request, "medical_need.html", {})


def non_medical_need(request, *args, **kwargs):
    return render(request, "nonmedicalneed.html", {})


def request_sent(request, *args, **kwargs):
    req = request.POST
    print(room_number)
    for key in req.keys():

        if key in emergency_medical_need_list or key in non_medical_need_list or key in question_list:
            try:
                patient_request = forms.Bell(message=messages[key][0],
                                             priority=messages[key][1],
                                             staff=messages[key][2],
                                             emergency=messages[key][3],
                                             room_number=room_number)
                patient_request.save()
            except:
                print("Could not find request type")
                # Do nothing

    return render(request, "request_sent.html", {})


def non_urgent_question(request, *args, **kwargs):
    return render(request, "nonurgentquestion.html", {})


def request_delete_view(request, rq_id):
    obj = get_object_or_404(Bell, id=rq_id)
    if request.method == "POST":
        obj.delete()
        return redirect('../')


def nurse_view(request):
    queryset = Bell.objects.all()
    this_minute = int(datetime.now().minute)

    for b in queryset:
        passed_minutes = 0
        if b.time is not None:
            passed_minutes = abs(b.time.replace(tzinfo=None) - datetime.now()).seconds/60
        if passed_minutes < 2:
            b.danger_mode = "green"
        elif 5 > passed_minutes >= 2:
            b.danger_mode = "yellow"
        else:
            b.danger_mode = "red"

    context = {
        'object_list': queryset
    }
    return render(request, "patient_request.html", context)