#!/usr/bin/env python2.4

"""
Some code for quick calculations fo rwave stuff for the DBL-152 spill

"""
import Waves as W
from math import pi
#import Numeric as N
import numarray as N
import matplotlib
import pylab
import datetime
from matplotlib.ticker import FormatStrFormatter, NullLocator,NullFormatter
import matplotlib.dates as Dates

g = 9.806
h = 50 / 3.281 #  ft to meters
#h = 70 / 3.28121.34 # ft to meters


# load Energy spectrum data:

#infilename = "WaveSpectrum2004-42035.txt"
#bins, Es, dates = W.ReadNDBCSpectrum(infilename)

# infilename = "WaveSpectrum-42035.txt"
#infilename = "WaveSpectrum-Dec05-2005-42035.txt"

## Figure 1
##infilename = "WaveSpectrum-Fig1.txt"
##outfilename = infilename[:-4]
##bins, Es, dates = W.ReadNDBCSpectrumRealTime(infilename)
##days = Dates.DayLocator((5,10,15,20,25,30))
##daysFmt= Dates.DateFormatter("%b-%d")   
##MaxVal = None

##Figure 2
##infilename = "WaveSpectrum-Fig2.txt"
##outfilename = infilename[:-4]
##bins, Es, dates = W.ReadNDBCSpectrum(infilename)
##days = Dates.MonthLocator()
##daysFmt= Dates.DateFormatter("%b-%y")   
##MaxVal = None

##Figure 3
infilename = "WaveSpectrum-Fig2.txt"
outfilename = infilename[:-5] + "3"
bins, Es, dates = W.ReadNDBCSpectrum(infilename)
days = Dates.MonthLocator()
daysFmt= Dates.DateFormatter("%b-%y")   
MaxVal = 20


dates = [ ([int(x) for x in i]) for i in dates ]
datetimes = [datetime.datetime(*i) for i in dates]

# convert bins (Hz) to k:
omega = 2 * N.pi * bins
k = W.WaveNumber(g, omega, h)

# convert to energy at the bottom:
Eb = Es / (N.sinh(k*h)**2)

##print "Energy at Top:",
##print Es[0:1]
##print "Energy at Bottom:",
##print Eb[0:1]
##print "Ratio:"
##print Eb[0:1] / Es[0:1]

# total energy
Etotal = N.sum(Eb, 1)# sum across rows

print "max energy", N.maximum.reduce(Etotal)

# Plot energy over time:
F = pylab.Figure()
ax = pylab.subplot(1,1,1)

#print "Position:", ax.get_position()
left, bottom, width, height = ax.get_position()
delta = 0.08
ax.set_position([left, bottom + delta, width, height-delta])

#pylab.plot(pylab.date2num(datetimes), Etotal )
#pylab.plot_date(pylab.date2num(datetimes), Etotal, "-" )
ax.plot_date(pylab.date2num(datetimes), Etotal, "-" )

ax.set_title("Total wave energy at the bottom at a depth of %i ft."%(h * 3.281,))

#Trim axis:
if MaxVal is not None:
    ax.set_ylim((0.0, MaxVal))

mindate = min(pylab.date2num(datetimes[-1]), (pylab.date2num(datetimes[0])) )
maxdate = max(pylab.date2num(datetimes[-1]), (pylab.date2num(datetimes[0])) )
ax.set_xlim( (mindate, maxdate) )


#noLabels = NullLocator()
#Labels = NullFormatter()
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(daysFmt)  

labels = ax.xaxis.get_ticklabels()
print labels
#print pylab.setp(labels)
print pylab.getp(labels[0], "fontsize")
##pylab.setp(labels,
##           rotation=45,
##           horizontalalignment='right',
##           dashlength=3,
##           dashpad=0,
##           fontsize=10)    

for l in labels:
    print "setting properties"
    l.set_rotation(45)
    l.set_horizontalalignment('right')
    l.set_dashlength(3)
    l.set_dashpad(0)
    l.set_fontsize(16)    

pylab.ylabel("Energy (m^2/Hz)")
pylab.grid('on')
print "Saving:", outfilename
Fig = pylab.gcf()
#Fig.set_figsize_inches( (5.75, 4.3) )
Fig.set_size_inches( (8, 6) )
##print pylab.gca().get_position()
ax.set_position([0.13,
                 0.14,
                 0.775,
                 0.77])
Fig.savefig(outfilename+".eps")
Fig.savefig(outfilename+".png", dpi=300)

pylab.show()

### find the amount of time value exceeded 6
Threshold = 6.0

Exceed = len(N.nonzero(Etotal > Threshold)[0])
print "Number of hours Energy greater than %f : %i"%(Threshold, Exceed )
print "Fraction of total: %f"%(float(Exceed) / len(Etotal) )


### Rob Naim's numbers:

## Hs(m)/Tp(s)/peak orbital velocity (cm/s)
## 2/6/33
## 2/9/57
## 4/6/66
## 4/9/115

##data = [(2, 6),
##        (2, 9),
##        (4, 6),
##        (4, 9)  ]

##for H, T in data:
##    Um = W.Max_u(H/2, 2.0*pi/T, g, h, -h)

##    print "Wave Height: %fm, Period: %fs, Max Velocity: %fm/s"%(H, T, Um)

### these match Rob's numbers pretty well

####Get the energy at the bottom:
##h0 = 13.7  # depth at bouy
##h = 15.24 # depth at ship location

#### Shoaling Coefficient
##Ks = W.ShoalingCoeff(2 * pi / 20, g, h0, h)
##print "Shoaling coeff for 20s wave: %f"%Ks
##print "That's close  enough to 1 to ignore"


##MaxTime  = N.argmax(Etotal)
##print "time of max Energy"
##print dates[MaxTime]
##MaxDay_s = Es[MaxTime]
##MaxDay_b = Eb[MaxTime]

###Equivalent wave height
##domega = omega[1] - omega[0] # this assumes the bins are all the same size!
##dHz = bins[1] - bins[0]
###print "domega:", domega

##Hmax_s = N.sqrt(8 * MaxDay_s * domega)
##Hmax_b = N.sqrt(8 * MaxDay_b * domega)
###Hmax_s = N.sqrt(8 * MaxDay_s * dHz)
###Hmax_b = N.sqrt(8 * MaxDay_b * dHz)
##print "Hmax_s:", Hmax_s 
##print "Hmax_b:", Hmax_b 

##Umax_s = Hmax_s/2 * omega
##Umax_b = Hmax_b/2 * omega


##Umax_s2 = W.Max_u(Hmax_s/2, omega, g, h, z = 0)
##Umax_b2 = W.Max_u(Hmax_b/2, omega, g, h, z = -h)

##print "Umax_b:",  Umax_b

##MaxU_i = N.argmax(Umax_b)

##print "During a storm on", dates[MaxTime]
##print "Maximum Wave height is: %.2f"%Hmax_s[MaxU_i]

##print "Maximum velocity at the surface is %.2f m/s:"%Umax_s[MaxU_i]
##print "Maximum velocity at bottom is %.2f m/s:"%Umax_b[MaxU_i]

##print "Maximum velocity at the surface is %.2f m/s:"%Umax_s2[MaxU_i]
##print "Maximum velocity at bottom is %.2f m/s:"%Umax_b2[MaxU_i]

##print "At a period of %.1f seconds"%(2*N.pi/omega[MaxU_i])
##print "The Wavelength at that period is %.1f meters"%(2*N.pi/k[MaxU_i])


