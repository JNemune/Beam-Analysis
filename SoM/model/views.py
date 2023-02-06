from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BeamForm
from .models import BeamModel, SupportModel


def beam_creator(request):
    if request.method == 'POST':
        cd = request.POST

        len=cd['len']
        unit_1=cd['unit1']
        f = cd['F']
        ft = cd['FT']
        w = cd['W']
        wt = cd['WT']
        unit_2=cd['unit2']

        if unit_1 == 'MM':
            len = len/1000
        elif unit_1 == 'IN':
            len = len*2.54/100
        elif unit_1 == 'FT':
            len = len/3.281

        if unit_2 == 'MM':
            f = f/1000
            ft = ft/1000
            w = w/1000
            wt = wt/1000
        elif unit_2 == 'IN':
            f = f*2.54/100
            ft = ft*2.54/100
            w = w*2.54/100
            wt = wt*2.54/100
        elif unit_2 == 'FT':
            f = f/3.281
            ft = ft/3.281
            w = w/3.281
            wt = wt/3.281

        BeamModel.objects.create(
                len=cd['len'],
                unit_1=cd['unit1'],
                f = cd['F'],
                ft = cd['FT'],
                w = cd['W'],
                wt = cd['WT'],
                unit_2=cd['unit2']
        )
    return redirect('beam')


def support_type(request):
    if request.method == 'POST':
        cd = request.POST
        type = cd['type']
        return render(request, 'model/support.html', {'type':type})
    else:
        return render(request, 'model/support.html', {'type':None})
    

def cantilevered(request):
    if request.method == 'POST':
        cd = request.POST
        len = float(cd['Can'])
        if cd['unit'] == 'MM':
            xpin = len/1000
        elif cd['unit'] == 'IN':
            xpin = len*2.54/100
        elif cd['unit'] == 'FT':
            xpin = len/3.281
        else:
            xpin = len

        SupportModel.objects.create(a = xpin, b=-1)

    return render(request, 'model/support.html')


def pinroller(request):
    if request.method == 'POST':
        cd = request.POST
        pin = float(cd['Pin'])
        if cd['unit_a'] == 'MM':
            xpin = pin/1000
        elif cd['unit_a'] == 'IN':
            xpin = pin*2.54/100
        elif cd['unit_a'] == 'FT':
            xpin = pin/3.281
        else:
            xpin = pin

        rol = float(cd['Rol'])
        if cd['unit_b'] == 'MM':
            xroller = rol/1000
        elif cd['unit_b'] == 'IN':
            xroller = rol*2.54/100
        elif cd['unit_b'] == 'FT':
            xroller = rol/3.281
        else:
            xroller = rol

        SupportModel.objects.create(a =xpin, b = xroller)
    return render(request, 'model/support.html')