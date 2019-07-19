import subprocess


def main(i):
    if i == 100:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_100.bat")
        p.communicate()

    elif i == 75:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_75.bat")
        p.communicate()

    elif i == 50:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_50.bat")
        p.communicate()

    elif i == 25:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_25.bat")
        p.communicate()

    elif i == 8:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_8.bat")
        p.communicate()

    elif i == 6:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_6.bat")
        p.communicate()

    elif i == 4:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_4.bat")
        p.communicate()

    elif i == 2:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh3_2.bat")
        p.communicate()
