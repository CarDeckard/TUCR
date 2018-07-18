import subprocess


def main(i):
    if i == 100:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_100.bat")
        p.communicate()

    elif i == 75:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_75.bat")
        p.communicate()

    elif i == 50:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_50.bat")
        p.communicate()

    elif i == 25:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_25.bat")
        p.communicate()

    elif i == 8:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_8.bat")
        p.communicate()

    elif i == 6:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_6.bat")
        p.communicate()

    elif i == 4:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_4.bat")
        p.communicate()

    elif i == 2:
        p = subprocess.Popen("C:/Users/jmcclurg/bat_files/ssh4_2.bat")
        p.communicate()