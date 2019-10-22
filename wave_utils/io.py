
"""
Assorted I/O functions

Only readers for a couple formats as of now.
"""

# py2/3 compatibility:
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime
import numpy as np


def ReadNDBCSpectrum(filename):

    """
    Note: this ignores gaps in the data
    """

    infile = open(filename, 'U')

    header = infile.readline()
    bins = np.array([float(x) for x in header.split()[4:]])

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

    # read and toss the header
    infile.readline()

    Dates = []
    Data = []
    Bins = []
    for line in infile:
        Dates.append(line.split()[:4])
        data = line.split()[6:]
        Data.append([float(data[i]) for i in range(0, len(data), 2)])
        if not Bins:
            Bins = ([float(data[i][1:-1]) for i in range(1, len(data), 2)])

    Data = np.array(Data, np.Float)
    Bins = np.array(Bins, np.Float)

    return (Bins, Data, Dates)

def read_NDBC_realtime_processed_data(filename):
    """
    reads the dat from the NDBC "real time" "spectral data" file

    (Not the "raw spectrum" file)

    it looks like this:

    #YY  MM DD hh mm WVHT  SwH  SwP  WWH  WWP SwD WWD  STEEPNESS  APD MWD
    #yr  mo dy hr mn    m    m  sec    m  sec  -  degT     -      sec degT
    2019 10 22 01 00  2.2  0.5 11.1  2.1  8.3 SSE ESE      STEEP  6.3 120
    2019 10 22 00 30  2.3  0.7 10.5  2.2  9.1 SSE  SE    AVERAGE  6.4 135
    2019 10 22 00 00  2.3  0.7 10.5  2.2  9.9 SSE SSE    AVERAGE  6.5 151
    2019 10 21 23 30  2.2  0.7 10.5  2.2  9.9 SSE SSE    AVERAGE  6.4 158
    2019 10 21 23 00  2.3  0.6 10.5  2.3  9.1 SSE  SE    AVERAGE  6.3 141
    2019 10 21 22 30  2.3  0.8 10.5  2.1  9.1 SSE  SE    AVERAGE  6.3 138
    ...
    """
    with open(filename) as infile:
        header = infile.readline().split()
        if header[6] != "SwH" or header[7] != "SwP":
            raise ValueError("file format not what is expected")
        infile.readline()
        times = []
        periods = []
        heights = []
        for line in infile:
            line = line.split()
            dt = [int(i) for i in line[:5]]
            times.append(datetime(*dt))
            periods.append(float(line[7]))
            heights.append(float(line[6]))

        return times, periods, heights






