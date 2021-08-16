#!/usr/bin/env python
# coding: utf-8

# Calculation of mobility, mean free path, etc.
# Julien Barrier
# julien.barrier@manchester.ac.uk
# @JulienBarrier

# header - do not change this
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
from matplotlib.colors import LogNorm
import scipy.ndimage
import seaborn as sns
import lmfit
import pandas as pd
import lmfit
from lmfit.models import LinearModel

# Change the variables below to match with measurement files

# General data
prefix = '' # prefix for the output files
raw_folder = '../raw/'# path to the folder with raw data
output_folder = '../data/' # where to store the exported datasets
figures_folder = '../plots/Figures/' #path to the figures

## experimental setup
gate_sweep = 'V_sweep_2636a_2nd_smub'
lockins = ['MFLI_X1','MFLI_X2','MFLI_X3'] #names of the lockins that appear in the folders
field = 'B_triton'
sep = '\t' # separator in the input files
ext = '.dat' # extension of the input files

## device data
Rxy = [False, True, False] # lockins that measure Rxy. put True or False, order of ´´lockins´´
Rxx = [True, False, True] # lockins that measure  Rxx. same Rxy
aspect_ratio = [.8/2.4,1,.8/.8] # ratio W/L for the different contact measured. put 1 for Rxy.
current = 10e-9 # input current in Amps.
field = .1 # field for hall measurements, in T (± for symmetrisation)
temperature = .01 # temperature in kelvin
contacts = ['23-4','9-2','9-7']

## files
year = '19' # year, only last two digits
month = 'July' # month, all letters
day = '13' # 2 digits, date of measurements
nb_zero_field = '006' # number of the file
nb_plus_field = '012'
nb_minus_field = '017'
path = raw_folder + month + '20' + year + '/' + month[:3] + day + year + '/'

## do not change below
# define useful functions

def find_dirs(d):
    "list the directories in directory d"
    import os
    return [os.path.join(d,o + '/').replace('\\','/') for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

def find_files_subdir(indir):
    scans = glob.glob(indir+'*/**/*.dat', recursive=True)
    print('found %s data files'%len(scans))
    return scans

def find_files(indir):
    scans = glob.glob(indir + '*.dat')
    print('found %s data files'%len(scans))
    return scans

def import_files(indir,fbase):
    list = find_files_subdir(indir,fbase);
    list.sort();
    files = [None] * len(list)
    for filenumber in range(len(list)):
        files[filenumber]= pd.read_csv('%s'%list[filenumber],sep='\t')
    del list

    return files

def sigma_xx(Rxx,Rxy,aspect_ratio):
    if len(Rxx) == len(Rxy):
        sig = [None]*len(Rxx)
        for i in range(len(Rxx)):
            sig[i] = (Rxx[i]*aspect_ratio) / ((Rxx[i]*aspect_ratio)**2 + (Rxy[i])**2)
        return sig
    else:
        print('error: Rxx and Rxy should be equal vectors')

def sigma_xy(Rxx,Rxy,aspect_ratio):
    if len(Rxx) == len(Rxy):
        sig = [None]*len(Rxx)
        for i in range(len(Rxx)):
            sig[i] = (Rxy[i]) / ((Rxx[i]*aspect_ratio)**2 + (Rxy[i])**2)
        return sig
    else:
        print('error: Rxx and Rxy should be equal vectors')

def muH(sigma,n):
    e = 1.6021766208e-19
    if len(sigma) == len(n):
        mu = [None]*len(sigma)
        for i in range(len(sigma)):
            mu[i] = np.abs(sigma[i]/n[i]/e)
        return mu
    else:
        print('error: sigma and n should be equal vectors')

def mean_free_path(sigma,n):
    e = 1.6021766208e-19
    hbar = 1.054571800e-34
    if len(sigma) == len(n):
        l = [None]*len(sigma)
        for i in range(len(sigma)):
            l[i] = hbar * np.sqrt(np.abs(np.pi / n[i])) / e**2 * sigma[i]
        return l
    else:
        print('error: sigma and n should be equal vectors')


e = 1.6021766208e-19
h = 6.626070040e-34

# figure parameters
sns.set(style='ticks',palette='Set2',rc={"axes.facecolor": (0, 0, 0, 0),'font.family': [u'Helvetica Neue'],
 'font.sans-serif': [u'Helvetica Neue']});
cmap = sns.color_palette('colorblind',6);
plt.style.use('default');
rcParams['axes.linewidth'] = .5;
rcParams['xtick.major.size'] = 2;
rcParams['ytick.major.size'] = 2;
rcParams['xtick.major.width'] = .5;
rcParams['ytick.major.width'] = .5;
rcParams['xtick.direction'] = 'in';
rcParams['ytick.direction'] = 'in';
rcParams['xtick.top'] = True;
rcParams['ytick.right'] = True;
rcParams['xtick.labelsize'] = 8;
rcParams['ytick.labelsize'] = 8;
rcParams['axes.labelsize'] = 8;
rcParams['figure.constrained_layout.use'] = True;
rcParams['figure.constrained_layout.hspace'] = 0;
rcParams['figure.constrained_layout.wspace'] = 0;
rcParams['figure.constrained_layout.h_pad'] = 1/72;
rcParams['figure.constrained_layout.w_pad'] = 1/72;
fig_ratio = (11.69,8.27); #A4 format

#start of the program

lockin_res_xx = []
lockin_res_xy = []
for i in range(len(Rxx)):
    if Rxx[i]:
        lockin_res_xx.append(lockins[i])
    elif Rxy[i]:
        lockin_res_xy.append(lockins[i])
    else:
        pass

zero_field = pd.read_csv(path + month[:3] + day + year + 'x' + nb_zero_field + ext,sep=sep)
plus_field = pd.read_csv(path + month[:3] + day + year + 'x' + nb_plus_field + ext,sep=sep)
minus_field = pd.read_csv(path + month[:3] + day + year + 'x' + nb_minus_field + ext,sep=sep)

# hall table = extract different data from the hall measurements.
hall = pd.DataFrame({'Rxy +%s T'%field: plus_field[lockin_res_xy[0]].values/current,
                     'Rxy -%s T'%field: minus_field[lockin_res_xy[0]].values/current },
                    index = plus_field[gate_sweep])
hall['Rh'] = pd.Series([ (hall['Rxy +%s T'%field].values[i] - hall['Rxy -%s T'%field].values[i]  ) /2 for i in range(len(hall))],
                      index = hall.index)
hall['n'] = pd.Series([field/hall['Rh'].values[i]/e for i in range(len(hall))],
                     index = hall.index)

hall.to_csv(output_folder + month[:3] + day + prefix + '_preliminary_hall_' + str(int(field*1000)) + 'mT.csv')

x_fit_min = int(len(hall)/3)
x_fit_max = int(2*len(hall)/3)

x_fit = [hall.index[i] for i in range(x_fit_min,x_fit_max)]
y_fit = [hall.n.values[i] for i in range(x_fit_min,x_fit_max)]

linmod = LinearModel()
linmod.set_param_hint('intercept',value=1e16)
linmod.set_param_hint('slope',value=1e16)
linout = linmod.fit(y_fit, x = x_fit)

print('equation y = ax+b')
print('a = %s 10¹² cm⁻²/V'%np.round(linout.params['slope'].value/1e16))
print('b = %s 10¹² cm⁻²'%np.round(linout.params['intercept'].value/1e16))

y_t = np.linspace(int(hall.index.min()),int(hall.index.max()),10)

plt.figure(figsize=(6,6),dpi=120)

slope = ( linout.params['slope'].value)
intercept = (linout.params['intercept'].value)

plt.plot(hall.index,(hall.n)/1e16,'-',color='r',marker='.',markersize=2,linewidth=0,label = '$n$')
plt.plot(y_t,(y_t*slope + intercept)/1e16,'y-',linewidth=1,label='fit')

plt.axvline(hall.index[x_fit_max],color='b')
plt.axvline(hall.index[x_fit_min],color='b')

plt.xlim(int(hall.index.min()),int(hall.index.max())),
plt.ylim(-3,3)
plt.legend(facecolor='k',loc=4,fontsize='14')
plt.ylabel('carrier density, $n\quad$(10⁻¹⁶ m⁻²)')
plt.xlabel('back gate voltage, $V_{BG}\quad$(V)')

plt.text(-35,2.5,'$y = (%.1e) * x + %.1e$'%(slope,intercept),size=14,verticalalignment='top')

plt.show()


# metrics table: get the carrier density, mobility, mean free path etc.


metrics = pd.DataFrame({'Rxx %s'%i: zero_field[i].values/current for i in lockin_res_xx},
                    index = zero_field[gate_sweep])

for j in lockin_res_xy:
    metrics['Rxy %s'%j] = pd.Series(zero_field[j].values/current, index = metrics.index)

metrics['n'] = pd.Series(-(zero_field[gate_sweep].values * slope + intercept), index = metrics.index)

lockin_aspect_ratio = {}
labels = {}
for i in range(len(lockins)):
    if Rxx[i]:
        lockin_aspect_ratio[lockins[i]] = aspect_ratio[i];
        labels[lockins[i]] = contacts[i]

for i in lockin_res_xx:
    for j in lockin_res_xy:
        metrics['σxx %s-%s'%(i[-2:],j[-2:])] = pd.Series(
            sigma_xx(metrics['Rxx %s'%i].values,metrics['Rxy %s'%j].values,lockin_aspect_ratio[i]),
            index = metrics.index)

for i in lockin_res_xx:
    metrics['μH %s-%s'%(i[-2:],j[-2:])] = pd.Series(
        muH(metrics['σxx %s-%s'%(i[-2:],j[-2:])].values,metrics.n.values),
        index = metrics.index
    )

for i in lockin_res_xx:
    metrics['le %s-%s'%(i[-2:],j[-2:])] = pd.Series(
        mean_free_path(metrics['σxx %s-%s'%(i[-2:],j[-2:])].values,metrics.n.values),
        index = metrics.index
    )

# display this as a figure and save it as a pdf file

fig, ax = plt.subplots(nrows=2,ncols=3,figsize=fig_ratio)

ax[0,0].plot(hall.index,hall.Rh,c=cmap[0])
ax[0,0].set_xlabel('back gate voltage, $V_{BG}\quad$(V)')
ax[0,0].set_ylabel('Hall resistance at %smT, $R_H\quad$(Ω)'%int(field*1000))
ax[0,1].set_xlim(int(hall.index.min()),int(hall.index.max()))

ax[0,1].plot(hall.index,(hall.n)/1e16,c=cmap[1],marker='.',markersize=2,linewidth=0,label = '$n$')
ax[0,1].plot(y_t,(y_t*slope + intercept)/1e16,c=cmap[2],linewidth=1,label='fit')

ax[0,1].axvline(hall.index[x_fit_max],c=cmap[0])
ax[0,1].axvline(hall.index[x_fit_min],c=cmap[0])

ax[0,1].set_xlim(int(hall.index.min()),int(hall.index.max())),
ax[0,1].set_ylim(-3,3)
ax[0,1].legend(loc=4,fontsize='small')
ax[0,1].set_ylabel('carrier density, $n\quad$(10⁻¹⁶ m⁻²)')
ax[0,1].set_xlabel('back gate voltage, $V_{BG}\quad$(V)')
ax[0,1].text(-35,2.6,'$n = (%.1e) * V_g  + %.1e$'%(slope,intercept),verticalalignment='top',bbox = dict(facecolor='w',edgecolor='k'),color='k')

k=0
for i in lockin_res_xx:
    k += 1
    ax[0,2].semilogy(metrics.n/1e16, metrics['Rxx %s'%i]*lockin_aspect_ratio[i],label=labels[i],c=cmap[k])
    for j in lockin_res_xy:
        ax[1,0].plot(metrics.n/1e16,metrics['σxx %s-%s'%(i[-2:],j[-2:])],c=cmap[k])
        ax[1,1].plot(metrics.n/1e16,metrics['μH %s-%s'%(i[-2:],j[-2:])]/100,c=cmap[k])
        ax[1,2].plot(metrics.n/1e16,metrics['le %s-%s'%(i[-2:],j[-2:])]*1e6,c=cmap[k])
ax[0,2].set_ylabel('Longitudinal resistance, $R_{xx}\quad$(Ω)')
ax[0,2].legend(title='contacts',loc=1,fontsize='small')
ax[0,2].set_xlim(metrics.n.min()/1e16,metrics.n.max()/1e16)
ax[0,2].set_xlabel('carrier density, $n\quad$(10⁻¹² cm⁻²)')


for k in range(3):
    ax[1,k].set_xlim(metrics.n.iloc[x_fit_min]/1e16,metrics.n.iloc[x_fit_max]/1e16)
    ax[1,k].set_xlabel('carrier density, $n\quad$(10⁻¹² cm⁻²)')
ax[1,0].set_ylabel('conductivity, $\sigma_{xx}\quad$(S)')
ax[1,1].set_ylabel('mobility, $\mu_H\quad$(10⁶ cm²/V)')
ax[1,2].set_ylabel('mean free path, $l_e\quad$(μm)')

plt.savefig(figures_folder + month[:3] + day + prefix + '_preliminary_' + str(int(current*1e9)) + 'nA' + str(int(temperature*1000)) + 'mK.pdf')
