#py2/3 compatible:
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Assorted I/O functions

Only readers for a couple formats as of now.
"""

def ReadNDBCSpectrum(filename):

    """
    Note: this ignores gaps in the data
    """
    
    infile = open(filename, 'U')

    header = infile.readline()
    bins = np.array([float(x) for x in header.split()[4:]])
    #print "bins:", bins

    Dates = []
    Data = []
    for line in infile:
        Data.append([float(x) for x in line.split()[4:]])
        Dates.append(line.split()[:4])

    Data = np.array(Data, np.Float)

    return (bins, Data, Dates)

def ReadNDBCSpectrumRealTime(filename):

    """

    This reads the "real time" NDBC data, which is a different format than
    the archive data.
    
    Note: this ignores gaps in the data

    """
    
    infile = open(filename, 'U')

    header = infile.readline()
    #bins = np.array([float(x) for x in header.split()[4:]])
    #print "bins:", bins

    Dates = []
    Data  = []
    Bins  = []
    for line in infile:
        Dates.append(line.split()[:4])
        data = line.split()[6:]
        Data.append([float(data[i]) for i in range(0,len(data),2)])
        if not Bins:
            Bins = ([float(data[i][1:-1]) for i in range(1,len(data),2)])

    Data = np.array(Data, np.Float)
    Bins = np.array(Bins, np.Float)

    return (Bins, Data, Dates)
