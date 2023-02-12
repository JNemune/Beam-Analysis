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
    reactions = instance.reactions()
    loads = instance.loadings()
    
    base = "/var/www/html/static/home/"
    loads[0].savefig(base + 'loads1.png')
    loads[1].savefig(base + 'loads2.png')
    instance.bending_plot().savefig(base + 'plt.png')
    instance.normal_stress_max_plot().savefig(base + 'sigma.png')
    instance.tau_y_max_plot().savefig(base + 'tau_y.png')
    instance.tau_xy_max_plot().savefig(base + 'tau_xy.png')
    instance.torque_plot().savefig(base + 'torque.png')
    
    latex = instance.bending()
    BG = instance.beam_geom()

    latex['normal_stress_max']=instance.normal_stress_max()
    latex['tau_y_max']=instance.tau_y_max()
    latex['tau_xy_max']=instance.tau_xy_max()
    latex['torque']=instance.torque()

    a = latex['w']
    b = latex['V']
    c = latex['M']
    d = latex['normal_stress_max']
    e = latex['tau_y_max']
    f = latex['tau_xy_max']
    g = latex['torque']
    h = BG['ybar']
    i = BG['ymax']
    j = BG['Iyy']
    k = BG['Izz']

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
    tau_y_max = formatter(e)
    tau_xy_max = formatter(f)
    torque = formatter(g)
    ybar = formatter(h)
    ymax = formatter(i)
    Iyy = formatter(j)
    Izz = formatter(k)

    latex_plotter = tex_plot(w, v, m, sigma_max, tau_y_max, tau_xy_max, torque, ybar, ymax, Iyy, Izz)
    return render(request, 'home/proj2.html', {'result': 1, 'info': reactions})
