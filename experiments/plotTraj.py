#!/usr/bin/env python

"""
Sample code from Matt

"""


from Hazmat.TAP import TAP_mod
import pylab as p
from matplotlib.ticker import FormatStrFormatter, NullLocator,NullFormatter
from matplotlib.dates import MonthLocator, WeekdayLocator, DayLocator, HourLocator, DateFormatter, MONDAY
from matplotlib.patches import Rectangle
import glob, os
import Numeric as N
import MA
import MLab
import random
from matplotlib import font_manager
import datetime
import string, struct
# import plotExt

def main():
    
    def gen_random():
        rand = random.random()    
        return rand    
    
    def readTrajTime(trajTime):
        moStr = 'January,February,March,April,May,June,July,August,September,October,November,December'
        moList = moStr.split(',')
#         moNum = range(12)
        
        trajTime.replace(',', ' ')
#         print 'trajTime', trajTime     
        mo, day, year, hourMin = trajTime.split()
#         print hourMin
        day = day.strip(',')
        hour, minute =  hourMin.split(':')
        moNum = moList.index(mo)+1            
        
#         print year, moNum, day, hour, minute
        
#         print 'Is this November?', moNum
        dtime = datetime.datetime(int(year),int(moNum),int(day),int(hour),int(minute))
        print dtime
        return dtime     
    
    def readGBinary(filename):
        
        import datetime
        
        header_format = '>10shhhhhffl'
        le_format = '>ffffflll'
        #     
        file = open(filename,'rb')
        #     
        header = file.read(struct.calcsize(header_format))
        (version1,day,month,year,hour,minute,current_time,version2,num_LE) = struct.unpack(header_format,header)

        position = N.zeros((num_LE,2),N.Float)
        latMSN = N.zeros((1,3),N.Float)
        
        rsize    = struct.calcsize(le_format) 

                
        # Loop through LaGrangian elements.
        for n in xrange(num_LE):   
            record = file.read(rsize)    
            (Lat,Long,Release_time,AgeWhenReleased,BeachHeight,nMap,pollutant,WindKey)= struct.unpack(le_format,record)        
    #         if Lat < 30.:
            position[n,:] = Lat, Long

#         latMSN[0,0] = sum(position[:,0])/len(position[:,0])
#     #     print latMSN[0,0]
#         latMSN[0,1] = min(position[:,0])
#         latMSN[0,2] = max(position[:,0])
        
        latMSN[0,0] = sum(position[:,0])/len(position[:,0])
    #     print latMSN[0,0]
        latMSN[0,1] = sum(position[:,0])/len(position[:,0]) - min(position[:,0])
        latMSN[0,2] = max(position[:,0]) - sum(position[:,0])/len(position[:,0])
        
#         [min(position[:,0]), max(position[:,0]), sum(position[:,0])/len(position[:,0])]
            
        record_time = datetime.datetime(year,month,day,hour,minute)
        return record_time, position, latMSN
    
    def buildTimeSeries():
        
        ls = glob.glob('obs/*')    
        print ls
        ls.sort()
        
        Lat= N.zeros((1,3),N.Float)
        count = 0
        
        for gbf in ls:        
        #     print gbf[-5:]
            if '.gbin' == gbf[-5:]:
        #         print '\n', gbf
                
                time, position, latMSN = readGBinary(gbf)       
                
                    
                if latMSN[0,0] == 0. or latMSN[0,0] > 999. :
                    print 'bad bounds', gbf
                    print 'latMSN', latMSN                        
                    print '\n'
                    pass
                else:
                    if count == 0.:
                        Lat2 = latMSN
                        Time = [time]
                        File = [gbf]
                    else:               
#                         print 'latMSN', latMSN             
                        Time.append(time)
                        File.append(gbf)
                        Lat2 = N.concatenate((Lat,latMSN),0)
                    count+=1                
                    Lat = Lat2
        return Time,Lat         
    
    def writeGbin(file, Trajectory,(NumTimesteps,NumLEs),HeaderData):
        """
            Write out binary splot file.
            'posLonLat' is list of (lon,lat)
            'lon' is positive to the west.
        """   
        def normal2ossm(year,month,day,hour,minute):
            """ 
                Calculation of OSSM time (hours since reference year to present year).
                Reference year is most recent year divisible by 4.  
            """
            #         import datetime
        
            year    = int(year)
            month   = int(month)
            day     = int(day)
            hour    = int(hour)
            
            modYear = year % 4 # modulus returns remainder
            refYear = year - modYear # present year less remainder
            refYear = datetime.datetime(refYear,1,1,0,0)
            nowTime = datetime.datetime(year,month,day,hour,minute)
            timeDiff= nowTime - refYear
            hoursDiff = timeDiff.days * 24. + (timeDiff.seconds/3600.)
            return hoursDiff         
                
        print 'timesteps, ', NumTimesteps,  ' NumLEs, ', NumLEs
        print HeaderData["Run duration"]
               
        nle = ':'

#         print NumLEs
        Latitude = N.ones((NumLEs,NumTimesteps),N.Float)
        Longitude= Latitude
    #     print maxLat
        for n in range(NumLEs):
            Lat = []
            Lon = []    
            count = 0
            t = []
        #     print n,Trajectory[:,n,:]
        # for lon, lat in Trajectory[0,:,:]:
        #     print lon,lat
            for lat, lon in Trajectory[:,n,:]:     
                t.append(count)
                Lat.append(lat)
                Lon.append(lon)
    #             N.put(maxLat,(n,:count),Lat)            
                count+=1
                
                        
            Latitude[n,:] = Lat                    
            Longitude[n,:] = Lon                    
                
        lt = HeaderData['Model start time']
        dt = readTrajTime(lt)
#         print lt
#         print dt
            
        timesteps = len(Trajectory[:,0,:])
                   
        for n in range(timesteps):
            
            stepInSeconds = float(n)*3600
#             print stepInSeconds
            
            timeLEout = dt + datetime.timedelta(seconds=stepInSeconds)
            
        
            year,month,day,hour,minute = timeLEout.year,timeLEout.month,timeLEout.day,timeLEout.hour,timeLEout.minute
            #
            #GNOME FORMATTING
            #
            header_format = '>10shhhhhffl'
            le_format = '>ffffflll'
            
            gnome_binary_name = file+'_'+str(year)+string.zfill(month,2)+string.zfill(day,2)+string.zfill(hour,2)+string.zfill(minute,2)+'.gbin'    
            
            gbfolder = file[:-5] #'fgbin_'+           
#             os.mkdir(gbfolder)
            gbpath = os.path.join(gbfolder,gnome_binary_name)
            
            my_file = open(gbpath,'wb') # write binary file
            
            
            version1 = 'HABTEST4U2'
            minute = 0
            current_time = normal2ossm(year,month,day,hour,minute) # requires integer input?
            version2 = 1.0
            
            year = float(year)
            month = float(month)
            day = float(day)
            hour = float(hour)
            minute= float(minute)
            #
            # Write Header
            #  
            headerData = struct.pack(header_format,version1,day,month,year,hour,minute,current_time,version2,NumLEs)
            my_file.write(headerData)
        #     print version1,day,month,year,hour,minute,current_time,version2,num_LE
        #     position = N.zeros((num_LE,2),N.Float)
        #     rsize    = struct.calcsize(le_format) 
            Release_time = current_time
            AgeWhenReleased = 0.0
            BeachHeight = 0.0
            nMap = 1
            pollutant = 9
            WindKey = 0
            
            lat = N.take(Latitude,(n,),1)
            lon = N.take(Longitude,(n,),1)
            # Loop through LaGrangian elements.
            for slat,slon in zip(lat,lon):   
        #         record = file.read(rsize)    
        #         (Lat,Long,Release_time,AgeWhenReleased,BeachHeight,nMap,pollutant,WindKey)= struct.unpack(le_format,record)        
        #         position[n,:] = Lat, Long
        #         print posLonLat[n]
    
    #             lon = posLonLat[n][0] * -1.0 # The data is negative for west but GNOME expects positive.
                leData =  struct.pack(le_format,slat,slon,Release_time,AgeWhenReleased,BeachHeight,nMap,pollutant,WindKey)
                my_file.write(leData)
        #         print
        return Latitude, Longitude
    # fname = glob.glob('*_b*nc.bout')
    
    print 'Input identifying string for .bout files such as, \'*_b*\', or more specifically as, \'*_CHL_b*\' or \'*_ANO_b*\.  If None given then \'*.bout\' is identifier.'
    idStr = raw_input('--> ')
#     idStr = '*_CHL_b*'
#     print 'idstr', idStr
        
    if idStr == '':
        fname = glob.glob('*.bout')    
    else:        
        fname = glob.glob(idStr+'.bout')

    # fn2 = glob.glob('*_b*_h36.cts_0.067*.bout')#'*_b*nc.bout'
    # fn2 = []
    fnT = fname+[]
    # fnT = fname+fn2
    # fnameglob.glob('*_b*.bout')
    #fname = ['cats_b', 'cats_c', 'dgom_b', 'dgom_c']
    print fnT
    raw_markers = ['1' , '2' , '3' , '4' , '<' , '>' , 'D' , 'H' , '^' , 'd' , 'h' , 'o' , 's' , 'v' , 'x']#'p', '|', '_' , ',' , '.' ,'+' ,
    markers = raw_markers[:]    
    linehands = []
#     print linehands
    RGB = []
    for n, c in enumerate(range(len(fnT))):
        rval=gen_random()
        gval=gen_random()
        bval=gen_random()
        #         cstep = .8/len(fnT)
        #         cval = n*cstep
        #         rval = 0.9 - cval
        #         gval = 0.1 + cval
        #         bval = 0.45 - ((0.45 - cval)/2) + cval
        rgb = (rval,gval,bval)
        RGB.append(rgb)        
    print RGB, '\n'
        
        
    p.figure(1)
    ax = p.axes([.15, .15, .65, .75], axisbg = 'w')    
    p.ioff()
    p.ylabel('Latitude')
    p.xlabel('Time [Month-Day]')
    p.title('Ensemble Results')
    days = DayLocator()
    daysFmt= DateFormatter("%m-%d")   
    noLabels = NullLocator()
    Labels = NullFormatter()
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)      
    latFmt = FormatStrFormatter('%5.2f')
    ax.yaxis.set_major_formatter(latFmt)  
        
    width_all = 1.
            
    xmin = None
    
    if 'obs' in os.listdir(os.getcwd()):        
        oTime,oLat = buildTimeSeries()    
             
    #     print Time,Lat
    #     print Lat[:,0]
    #     print Lat[:,1]
    #     print Lat[:,2]
    # 
    #     p.plot(p.date2num(Time),Lat[:,0], 'o', markersize=15., markerfacecolor=None, markeredgecolor = 'k', markeredgewidth=.5)
    #     p.plot(p.date2num(Time),Lat[:,1], 'x', markersize=15., markerfacecolor=None, markeredgecolor = 'k', markeredgewidth=.5)
    #     p.plot(p.date2num(Time),Lat[:,2], '+', markersize=20., markerfacecolor=None, markeredgecolor = 'k', markeredgewidth=.5)
    #     
        asyError = [oLat[:,1],oLat[:,2]] # lat[:,1:3]
        yline, eline = p.errorbar(p.date2num(oTime),oLat[:,0], asyError, None,'ob',ms=20.,mec='b',mfc=None, mew=width_all, capsize=width_all*10)
        
        set(eline,linewidth=5.)        
        
        xmin = min(oTime)
        xmax = max(oTime)                       
    print oTime
    for nfnT,file in enumerate(fnT):
        ocTime = oTime
        ocLat = oLat
        print file
        gbfolder = file[:-5]            #'fgbin_'+
#         print glob.glob(gbfolder+'*')
        gbstat = gbfolder+'.stat'
        fs = open(gbstat,'w')
                        
        if gbfolder in os.listdir(os.getcwd()):        
            old_gbs = os.listdir(gbfolder)            
            for old_gb in old_gbs:
                frm = os.path.join(gbfolder,old_gb)
                os.remove(frm)
            os.rmdir(gbfolder)
        os.mkdir(gbfolder)    
        
        (Trajectory,(NumTimesteps,NumLEs),HeaderData,flags) = TAP_mod.ReadTrajectory(file)
            
        print HeaderData

        modelStartTime = readTrajTime(HeaderData['Model start time'])

        Latitude,Longitude = writeGbin(file,Trajectory,(NumTimesteps,NumLEs),HeaderData)#,flags
                
        mxLat = N.ones((NumTimesteps),N.Float)
        meanLat = N.ones((NumTimesteps),N.Float)
        mnLat = N.ones((NumTimesteps),N.Float)
        leTimes = []
        
        # Assumming a Timestep is an hour (3600 seconds)!
        count = 0        
        for cn in range(NumTimesteps):
            dtime = datetime.timedelta(seconds=cn*3600)
            time  = modelStartTime + dtime
            tLat = N.take(Latitude,(cn,), 1)
    #         print tLat
            mxL = MA.maximum(tLat,)
            mnL = MA.minimum(tLat,)            
            meanL=MLab.mean(tLat,0)    
            N.put(mxLat,cn,mxL)            
            N.put(mnLat,cn,mnL)
            N.put(meanLat,cn,meanL)
            leTimes.append(time)
            
            nboth = 0
            if time in ocTime:
                write_matches = 1
                while write_matches == 1:
#                     print nboth, cn                     
                    if count == 0:
                        nboth = ocTime.index(time)
                        count +=1                        
#                         fs.write('%i, %s, %i %i %i %i %i, %f %f %f, %f %f %f\n'%(cn, file, int(time.year), int(time.month), int(time.day), int(time.hour), int(time.minute), mxL, meanL, mnL, ocLat[nboth,0], ocLat[nboth,1],ocLat[nboth,2]))
                    else:
                        try:
                            nboth = ocTime.index(time,nboth+1)                        
                        except ValueError:                            
                            write_matches = 0
                            pass
                    if write_matches == 1:
#                         fs.write('%s, %i, %i %i %i %i %i, %f %f %f, %f %f %f\n'%(file, cn, int(time.year), int(time.month), int(time.day), int(time.hour), int(time.minute), mxL, meanL, mnL, ocLat[nboth,0], ocLat[nboth,1],ocLat[nboth,2]))
                        
                        fs.write('%s, %i, %s, %f %f %f, %f %f %f\n'%(file, cn, str(time), mxL, meanL, mnL, ocLat[nboth,0], ocLat[nboth,1],ocLat[nboth,2]))                        
        if len(markers) == 0:
            markers = raw_markers[:]             
        
        random_marker = random.randrange(0,len(markers),1)            
        nmarker = markers[random_marker]        
        markers.pop(random_marker)            

        tn = p.date2num(leTimes)
        
        p.plot(tn,mxLat, '-', linewidth=width_all, color = RGB[nfnT])

        l1 = p.plot(tn[::24], mxLat[::24], 'o', markersize=9., marker=nmarker, markerfacecolor=None, markeredgecolor = RGB[nfnT], markeredgewidth=width_all)
        linehands.append(l1)        
        
        p.plot(tn,mnLat, '-', linewidth=width_all, color = RGB[nfnT])            
        p.plot(tn[::24], mnLat[::24], 'o', markersize=9., marker=nmarker, markerfacecolor=None, markeredgecolor = RGB[nfnT], markeredgewidth=width_all)
        
        p.plot(tn,meanLat, '-', linewidth=width_all, color = RGB[nfnT])          
        p.plot(tn[::24], meanLat[::24], 'o', markersize=9., marker=nmarker, markerfacecolor=None, markeredgecolor = RGB[nfnT], markeredgewidth=width_all)

        labels = ax.xaxis.get_ticklabels()   
        
        p.setp(labels, rotation=45, horizontalalignment='right',dashlength=3,dashpad=0)    
           
        if xmin == None:
            xmin = leTimes[0]
            xmax = leTimes[-1]
        else:
            if leTimes[0] < xmin:
                xmin = leTimes[0]
            if leTimes[-1] > xmax:
                xmax = leTimes[-1]                
                    
    xdmin = datetime.datetime(xmin.year,xmin.month,xmin.day)
    xdmax = datetime.datetime(xmax.year,xmax.month,xmax.day) 
    xnmin = p.date2num(xdmin)
    xnmax = p.date2num(xdmax)
    
    # Edge of grid impacts on trajectory probable.
    p.fill([xnmin,xnmin,xnmax,xnmax,xnmin],[25.0, 25.25, 25.25, 25.0, 25.0],facecolor='red')
    p.xlim((xnmin,xnmax))
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    p.ylim((25.0,28.5))
    yaxlim = p.ylim()
    xaxlim = p.xlim()
     
    # LOCATION AXIS
    axB = p.twinx() 
    axB.xaxis.set_major_locator(days)
    axB.xaxis.set_major_formatter(daysFmt)    
    labels = axB.get_xticklabels()
    p.setp(labels, rotation=45, horizontalalignment='right',dashlength=3,dashpad=0)    
  
    #Geolocation Degrees, Minutes.
    glDM = {'Cape Romano':[25,50], 'Naples':[26,10], 'Sanibel Island':[26,25], 'Venice Inlet':[27,8], 'Siesta Key':[27,15], 'Egmont Key':[27,35], 'Sand Key':[27,52], 'Tarpon Springs':[28,10], 'Bayport':[28,32], 'Crystal Bay':[28,53]}
    
    ytlocs = []
    ytlabels = []
    for loc, DM in glDM.iteritems():
        
        print 'Location: %s, Latitude (%i [deg], %i [min])'%(loc,DM[0],DM[1])
        ytlocs.append(float(DM[0])+float(DM[1])/60.)
        ytlabels.append(loc)
    
    p.ylim(yaxlim)    
    p.yticks(ytlocs,ytlabels)
    ticks = ax.yaxis.get_ticklines()    
    p.setp(ticks, markersize = 5)    
    p.xlim(xaxlim)
    
    p.savefig('ensPlot'+idStr+'.png')
    
    # LEGEND
    p.figure(2)
    
    ax2 = p.subplot(111)
    p.legend(linehands,fnT,'center',axespad=0.,pad=0.,markerscale=1.0,numpoints=1,handlelen=0.05, prop=font_manager.FontProperties(size='medium'))
    leg=p.gca().get_legend()
    leg.draw_frame(False)
    ax2.yaxis.set_major_locator(noLabels)
    ax2.yaxis.set_major_formatter(Labels)
    ax2.xaxis.set_major_locator(noLabels)
    ax2.xaxis.set_major_formatter(Labels)
    
    p.savefig('ensLeg'+idStr+'.png')     
    p.show()

main()
