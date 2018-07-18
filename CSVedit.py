"""
Created Tuesday July 10, 2018
With the purpose of processing experiment data into two easy to read graphs
(Power vs Percent CPU & Power vs Duration Time)
Authors: Josiah McClurg & Carson Deckard

Last Edited:
By:
"""
import numpy as np
import matplotlib.pyplot as plt


# Gathers data from the four runs to produce a graph of power vs percent CPU
# @folderName = folder experiment is stored in
def graphPowVsPerc(folderName):
    numCpuList = [2, 4, 6, 8]

    # Creates a header for the .csv file
    for run_num in [0, 1, 2, 3]:
        with open("%s/powVsPercGraph_Run%d.csv" % (folderName, run_num), 'w') as graphFile:
            np.savetxt(graphFile, np.array([[0] + numCpuList]), delimiter=",")

    # Fills the .csv
    for run_num in [0, 1, 2, 3]:
        with open("%s/powVsPercGraph_Run%d.csv" % (folderName, run_num), 'a') as graphFile:

            for percentCpu in [25, 50, 75, 100]:
                avgPowersList = []
                # for a fixed percentCpu:
                for numCpus in numCpuList:
                    # find the average across all runs:
                    currentCpuPercentAvgPowerList = []
                    fname = '%s/run%d_numCpu%d_cpuPct%d.csv'%(folderName, run_num, numCpus, percentCpu)

                    # Loads file into editable txt
                    timeNCurrentsNVoltage = np.loadtxt(fname, delimiter=",", skiprows=1)

                    # Creates four columns of voltage to be multiplied element by element by
                    # the current to get power readings
                    voltRepeat = np.tile(timeNCurrentsNVoltage[:,5], (4,1)).T
                    timeNPower = voltRepeat * timeNCurrentsNVoltage[:, 1:5]

                    # first mean averages across time within a single run.
                    # second mean averages across the computers
                    currentCpuPctAvgPower = timeNPower[:,1:].mean(axis=0,keepdims=True).mean()
                    currentCpuPercentAvgPowerList.append(currentCpuPctAvgPower)

                    # averages across all runs
                    avgCurrent = np.array(currentCpuPctAvgPower)
                    avgPowersList.append(avgCurrent)

                np.savetxt(graphFile, np.array([[percentCpu] + avgPowersList ]),delimiter=",")

        plotPoints = np.loadtxt("%s/powVsPercGraph_Run%d.csv" % (folderName, run_num), delimiter=',')
        num_cpus = plotPoints[0,1:]
        pct_cpu  = plotPoints[1:,0]
        avg_pwrs = plotPoints[1:,1:]

        plt.plot(pct_cpu,avg_pwrs)
        axes = plt.gca()
        axes.set_ylim([8, 10])
        axes.set_xlim([25, 100])
        axes.set_xticks([25, 50, 75, 100])
        plt.suptitle("Power vs Percent CPU")
        plt.ylabel("Power (Watts)")
        plt.xlabel("Percent CPU")
        plt.legend(["%d CPUs"%(c) for c in num_cpus], loc='upper left')
        plt.savefig('%s/PowerPercGraph%d.png'%(folderName, run_num))
        plt.close()

# Gathers data from the four runs to produce a graph of average power vs time taken
# @folderName = folder experiment is stored in
def graphPowVsTime(folderName):
    runNum = [0, 1, 2, 3]
    percentCpu = 100

    # Creates a Header for the .csv file
    #for a in runNum:
     #   with open("%s/powVsTimeGraph@%d_Run%d.csv" % (folderName, percentCpu, a), 'w') as graphFile:
      #      graphFile.write(",".join(['0']) + "\n")

    # Fills the .csv
    for a in runNum:
        with open("%s/powVsTimeGraph@%d_Run%d.csv" % (folderName, percentCpu, a), 'w') as graphFile:
            for numCpus in [2, 4, 6, 8]:
                energyList = []

                fname = '%s/run%d_numCpu%d_cpuPct100.csv'%(folderName, a, numCpus)

                # Loads file into editable txt
                timeNCurrentsNVoltage = np.loadtxt(fname, delimiter=",", skiprows=1)

                # Creates four columns of voltage to be multiplied element by element by
                # the current to get power readings
                voltRepeat = np.tile(timeNCurrentsNVoltage[:, 5], (4, 1)).T
                power = voltRepeat * timeNCurrentsNVoltage[:, 1:5]

                # Finds the average of the power used by each computer than sums them up
                # to get a single value for average power used overall
                powerAvgList = power.mean(axis=0,keepdims=True)

                powerAvg = sum(sum(powerAvgList[:]))

                # subtracts the start time by the last time recorded to find the total
                # time it took to run the experiment
                timeDiff = (timeNCurrentsNVoltage[-1, 0]) - (timeNCurrentsNVoltage[0, 0])

                energy = timeDiff * powerAvg

                energy = np.array(energy)
                energyList.append(energy)

                # saves values found to a .csv file for easily graphed data
                np.savetxt(graphFile, np.array([energyList]), delimiter=',')


        plotPoints = np.loadtxt("%s/powVsTimeGraph@%d_Run%d.csv" %(folderName, percentCpu, a), delimiter=',')
        cpusNums = ['2', '4', '6', '8']
        energyNums = plotPoints[:]
        plt.bar(cpusNums, energyNums)

        axes = plt.gca()
        axes.set_ylim([100, 160])
        plt.suptitle("Energy vs Number of CPUs")
        plt.ylabel("Energy (Joules)")
        plt.xlabel("Number of CPUs")
        plt.savefig('%s/TimeGraph%d.png'%(folderName, a))
        plt.close()



# Gathers data from the four runs to produce a graph of power vs percent CPU
# @folderName = folder experiment is stored in
def graphEnergyVsPerc(folderName):
    numCpuList = [2, 4, 6, 8]

    # Creates a header for the .csv file
    for run_num in [0, 1, 2, 3]:
        with open("%s/energyVsPercGraph_Run%d.csv" % (folderName, run_num), 'w') as graphFile:
            np.savetxt(graphFile, np.array([[0] + numCpuList]), delimiter=",")

    # Fills the .csv
    for run_num in [0, 1, 2, 3]:
        with open("%s/energyVsPercGraph_Run%d.csv" % (folderName, run_num), 'a') as graphFile:

            for percentCpu in [25, 50, 75, 100]:
                avgPowersList = []
                # for a fixed percentCpu:
                for numCpus in numCpuList:
                    # find the average across all runs:
                    currentCpuPercentAvgPowerList = []
                    fname = '%s/run%d_numCpu%d_cpuPct%d.csv'%(folderName, run_num, numCpus, percentCpu)

                    # Loads file into editable txt
                    timeNCurrentsNVoltage = np.loadtxt(fname, delimiter=",", skiprows=1)

                    # Creates four columns of voltage to be multiplied element by element by
                    # the current to get power readings
                    voltRepeat = np.tile(timeNCurrentsNVoltage[:,5], (4,1)).T
                    timeNPower = voltRepeat * timeNCurrentsNVoltage[:, 1:5]

                    # first mean averages across time within a single run.
                    # second mean averages across the computers
                    currentCpuPctAvgPower = timeNPower[:,1:].mean(axis=0,keepdims=True).mean()
                    currentCpuPercentAvgPowerList.append(currentCpuPctAvgPower)

                    timeDiff = (timeNCurrentsNVoltage[-1, 0]) - (timeNCurrentsNVoltage[0, 0])

                    # averages across all runs
                    avgCurrent = np.array(currentCpuPctAvgPower)
                    avgPowersList.append(avgCurrent * timeDiff)

                np.savetxt(graphFile, np.array([[percentCpu] + avgPowersList ]),delimiter=",")

        plotPoints = np.loadtxt("%s/energyVsPercGraph_Run%d.csv" % (folderName, run_num), delimiter=',')
        num_cpus = plotPoints[0,1:]
        pct_cpu  = plotPoints[1:,0]
        avg_energy = plotPoints[1:,1:]

        plt.plot(pct_cpu,avg_energy)
        axes = plt.gca()
        axes.set_ylim([28, 40])
        axes.set_xticks([25, 50, 75, 100])
        plt.suptitle("Energy vs Percent CPU")
        plt.ylabel("Energy (Joules)")
        plt.xlabel("Percent CPU")
        plt.legend(["%d CPUs"%(c) for c in num_cpus], loc='upper left')
        plt.savefig('%s/energyPercGraph%d.png'%(folderName, run_num))
        plt.close()

            # Used for standalone purpose. (mainly to test controlled revisions)
if __name__ == '__main__':
    graphEnergyVsPerc("exp_1531920712.41")