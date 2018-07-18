# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 03:04:57 2014
this is based very loosely on example code from the PyDAQmx website
@author: Josiah McClurg

Edited on Mon July 3, 2018
edited to perform a task specific to a summer research experiment
@editor: Carson Deckard
"""

import scipy.io
import time
import math
from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from PyDAQmx.DAQmxTypes import *

import numpy as np
from RingBuffer import *
import SSHIn1
import SSHIn2
import SSHIn3
import SSHIn4
import threading
import subprocess
import os ,errno
import CSVedit

class AIChannelSpec(object):
    def __init__(self, deviceName, portNum, name=None, termConf=DAQmx_Val_Cfg_Default, rangemin=-10, rangemax=10, units=None):
        self.port = 'ai%d'%(int(portNum))
        self.deviceName = str(deviceName)
        self.device = self.deviceName+'/'+self.port

        self.rangemin = float(rangemin)
        self.rangemax = float(rangemax)

        if name is None:
            self.name = 'v%d'%(int(portNum))
        else:
            self.name = str(name)

        self.termConf = termConf

        if not ((units is None) or (units.lower() == "volts") or (units.lower() == "volt") or (units.lower() == "v")):
            self.units = str(units)
            self.valType = DAQmx_Val_FromCustomScale
        else:
            self.units = None
            self.valType = DAQmx_Val_Volts


class MultiChannelAITask(Task):
    """Class to create a multi-channel analog input
    The channels must be a list of AIChannelSpec objects.
    """
    def __init__(self, channels, dataWindowLength=None, sampleRate=2000.0, bufferSize=None, sampleEvery=None, timeout=None,  data_updated_callback=None, debug=0):
        Task.__init__(self)

        self.debug = debug
        self.numChans = len(channels)
        self.timeStarted = -1
        self.timeStopped = -1
        self.data_updated_callback = data_updated_callback
        devicesReset = []

        for chan in channels:
            if chan.deviceName not in devicesReset:
                if self.debug > 0: print "Resetting device %s" % (chan.deviceName)
                DAQmxResetDevice(chan.deviceName)
                devicesReset.append(chan.deviceName)

            self.CreateAIVoltageChan(chan.device,
                        chan.name,
                        chan.termConf,
                        chan.rangemin,
                        chan.rangemax,
                        chan.valType,
                        chan.units)

        self.sampleRate = float(sampleRate)

        # The small memory buffer in which the samples go when they are read from the device.
        # The default is to make the buffer large enough to store a half second of data
        if bufferSize  is None:
            self.bufferSize = int(self.numChans*np.round(self.sampleRate/2.0))
        else:
            self.bufferSize = int(bufferSize)
        self.buffer = np.zeros(self.bufferSize)

        # The larger memory buffer to which the samples are added, for later viewing.
        # The default is large enough to store ten seconds of a data
        if dataWindowLength is None:
            self.dataWindow = RingBuffer(np.round(self.sampleRate*10.0),len(channels)+1);
        else:
            self.dataWindow = RingBuffer(dataWindowLength,len(channels)+1);

        # The default is chosen such that the buffer is half full when it is emptied
        if sampleEvery is None:
            self.sampleEvery = int(max(math.floor(math.floor(self.bufferSize/(self.numChans))/2.0),1))
        else:
            self.sampleEvery = int(sampleEvery)

        if timeout is None:
            self.timeout = float(self.sampleEvery)/self.sampleRate
        else:
            self.timeout = float(timeout)

        self.CfgSampClkTiming("OnboardClock",
                self.sampleRate,
                DAQmx_Val_Rising,
                DAQmx_Val_ContSamps,
                self.bufferSize)

        self.AutoRegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,
                self.sampleEvery,
                0)

        self.AutoRegisterDoneEvent(0)

    def EveryNCallback(self):
        read = int32()
        self.ReadAnalogF64(self.sampleEvery,
                self.timeout,
                DAQmx_Val_GroupByScanNumber,
                self.buffer,
                self.bufferSize,
                byref(read),
                None)

        endTime = time.time()
        numRead = int(read.value)
        if(numRead != self.sampleEvery):
            print '%d is not %d'%(numRead, self.sampleEvery)
            return -1

        startTime = endTime - float(numRead - 1)/self.sampleRate
        timeVector = np.linspace(startTime,endTime,numRead).reshape(numRead,1)
        readPortion = self.buffer[0:numRead*self.numChans].reshape(numRead,self.numChans)

        self.dataWindow.extend(np.concatenate((timeVector,readPortion),axis=1))
        if not (self.data_updated_callback is None):
            self.data_updated_callback(startTime,endTime,numRead)

        return 0

    def DoneCallback(self, status):
        return 0

    def StopTask(self):
        self.timeStopped = time.time()
        read = int32()
        self.ReadAnalogF64(-1,
                self.timeout,
                DAQmx_Val_GroupByScanNumber,
                self.buffer,
                self.bufferSize,
                byref(read),
                None)
        numRead = int(read.value)
        if numRead > 0:
            endTime = time.time()
            startTime = endTime - float(numRead)/self.sampleRate
            timeVector = np.linspace(startTime,endTime,numRead).reshape(numRead,1)
            readPortion = self.buffer[0:numRead*self.numChans].reshape(numRead,self.numChans)
            self.dataWindow.extend(np.concatenate((timeVector,readPortion),axis=1))

        Task.StopTask(self)

    def StartTask(self):
        self.timeStarted = time.time()
        Task.StartTask(self)


if __name__ == '__main__':
    import sys

    class flushfile():
        def __init__(self, f):
            self.f = f

        def __getattr__(self,name):
            return object.__getattribute__(self.f, name)

        def write(self, x):
            self.f.write(x)
            self.f.flush()

    # Make the output unbuffered
    sys.stdout = flushfile(sys.stdout)

    channels = []
    portNums = [0, 2, 4, 6, 17]
    # Pin 17 is GND
    # Changes the ports that are in use
    for i in portNums:
        c = AIChannelSpec('cDAQ1Mod1', i, termConf=DAQmx_Val_RSE, rangemin=-10, rangemax=10)
        channels.append(c)

    m = MultiChannelAITask(channels, sampleRate=2000, dataWindowLength=2000*50)
    folderName = "exp_%s"%(time.time())
    try:
        os.makedirs("C:\\Users\\jmcclurg\\PycharmProjects\\Phase0Tester\\%s"%folderName)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    print (" ________   __   __     ____   _____    \n"
           "|___  ___| |  | |  |  /   __| |      \  \n"
           "   |  |    |  | |  | |  /     |      /  \n"
           "   |  |    \  \ /  / |  \ __  |  |\  \  \n"
           "   |__|     \_____/   \_____| |__| \__\ \n")

    for runNum in range(4):
        print ("Run number %d"%runNum)

        for numCPUs in [8, 6, 4, 2]:
            # Where the numbers are the amount of virtual CPU per worker
            # The ones used have 8 virtual processors. May need to be changed
            SSHIn1.main(numCPUs)
            SSHIn2.main(numCPUs)
            SSHIn3.main(numCPUs)
            SSHIn4.main(numCPUs)

            for a in [100, 75, 50, 25]:
                # Where the numbers represent the percent CPU

                print ("%d vCPU running at %d percent"%(numCPUs,a))

                # SSH into all four workers to set their cpu percent cap
                print "Setting cpu cap..."
                SSHIn1.main(a)
                SSHIn2.main(a)
                SSHIn3.main(a)
                SSHIn4.main(a)

                # Starts reading from the NASDAQ
                m.StartTask()

                # Starts running the main target algorithm through Spark

                # Basic Stress program
                p = subprocess.Popen("C:\\cygwin64\\bin\\ssh.exe tucr@192.168.8.250 \"~/start_stress.sh\"")

                # Special Job
                # p = subprocess.Popen("Z:\\testing_index_vs_no_index \"~/no_index.py\"")

                p.communicate()

                # stops taking data
                m.StopTask()


                dat = {"startTime": m.timeStarted, "stopTime": m.timeStopped, "data": m.dataWindow.popFIFO(m.dataWindow.length)}
                dat['time'] = dat['data'][:,0] - dat['data'][0,0]
                for i in range(0, len(channels)):
                     dat[channels[i].name] = dat['data'][:, i+1]

                # Opens the correct directory to save files in
                f = open("%s/run%d_numCpu%d_cpuPct%d.csv"%(folderName,runNum,numCPUs,a), "w")

                # Scale amplified resistor voltages so that the result represents current (in amps) out of each server.
                # Scale is specific to project.
                dat['data'][:, 1] *= .2688
                dat['data'][:, 2] *= .2739
                dat['data'][:, 3] *= .2747
                dat['data'][:, 4] *= .2840
                np.savetxt(f, dat['data'], delimiter=',', header="Time (s), Computer 1 (A), Computer 2 (A), Computer 3 (A), Computer 4 (A), Voltage")
                f.close()

    CSVedit.graphPowVsPerc("C:/Users/jmcclurg/PycharmProjects/Phase0Tester/%s"%(folderName))
    CSVedit.graphPowVsTime("C:/Users/jmcclurg/PycharmProjects/Phase0Tester/%s"%(folderName))
    m.ClearTask()
