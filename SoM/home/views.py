from django.shortcuts import render, redirect
from django.http import HttpResponse
from .Beam import Beam
from model import models as mModels
from loads import models as lModels
from .mtpltlb import tex_plot


def homepage(request):
    return render(request, 'home/proj2.html', {'result': 0})


def beam_button(request):
    print('---------------')
    return render(request, 'model/Beam.html')


def supports_button(request):
    print('---------------')
    return render(request, 'model/support.html')


def forces_button(request):
    print('---------------')
    return render(request, 'loads/Force.html')


def moments_button(request):
    print('---------------')
    return render(request, 'loads/Moment.html')


def calculator(request):
    beam = mModels.BeamModel.objects.last()
    support = mModels.SupportModel.objects.last()
    forces = lModels.ForceModel.objects.all()
    moments = lModels.MomentModel.objects.all()

    Bdata = [
        beam.len,
        beam.f,
        beam.w,
        beam.ft,
        beam.wt,
        support.a,
        support.b
    ]
    if support.b < 0:
        Bdata[6] = None

    instance = Beam(Bdata[0], Bdata[1], Bdata[2],
                    Bdata[3], Bdata[4], Bdata[5], Bdata[6])

    for force in forces:
        Fdata = [force.x, force.y, force.x1, force.x2]
        if force.x2 < 0:
            Fdata[3] = None
        instance.floading(Fdata[0], Fdata[1], Fdata[2], Fdata[3])

    for moment in moments:
        Mdata = [moment.x, moment.z, moment.x1, moment.x2]
        if moment.x2 < 0:
            Mdata[3] = None
        instance.mloading(Mdata[0], Mdata[1], Mdata[2], Mdata[3])

    instance.calculate()
    instance.bending_plot().savefig(
        'C:/Users/Mohammad/Desktop/VSC/SoM/home/static/home/plt.png')
    instance.normal_stress_max_plot().savefig('C:/Users/Mohammad/Desktop/VSC/SoM/home/static/home/sigma.png')
    instance.torqe_plot().savefig('C:/Users/Mohammad/Desktop/VSC/SoM/home/static/home/torque.png')
    instance.tau_x_max_plot().savefig('C:/Users/Mohammad/Desktop/VSC/SoM/home/static/home/tau_x.png')
    latex = instance.bending()
    latex['normal_stress_max']=instance.normal_stress_max()
    latex['torque']=instance.torque()
    latex['tau_x_max']=instance.tau_x_max()
    reactions = instance.reactions()

    a = latex['w']
    b = latex['V']
    c = latex['M']
    d = latex['normal_stress_max']
    e = latex['torque']
    f = latex['tau_x_max']

    def formatter(x):
        for i in range(len(x)):
            if x[i] == '\\':
                if x[i+1] == '\\':
                    x.pop(i)

        return x

    w = formatter(a)
    v = formatter(b)
    m = formatter(c)
    sigma_max = formatter(d)
    torque = formatter(e)
    tau_x_max = formatter(f)

    latex_plotter = tex_plot(w, v, m, sigma_max, torque, tau_x_max)

    return render(request, 'home/proj2.html', {'result': 1, 'info': reactions})
