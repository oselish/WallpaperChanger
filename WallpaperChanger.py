import os
import ctypes
import datetime
import time
import subprocess

#текущий год:          now.year
#Текущий месяц:        now.month
#Текущий день:         now.day
#Текущий час:          now.hour
#Текущая минута:       now.minute
#Текущая секунда:      now.second
#Текущая микросекунда: now.microsecond
#Текущая дата и время с использованием strftime:  print now.strftime("%d-%m-%Y %H:%M")
#Текущая дата и время с использованием isoformat: print now.isoformat()


data = []
folder = ""
morning = ""
day = ""
evening = ""
night = ""
error = ""
cooldown = 0
def update():
    global folder, morning, day, evening, night, error, data, cooldown
    config = open("config.txt")
    while True:
        temp = config.readline()
        if not(temp.startswith("#")) and temp != "\n":
            if temp == "":
                break
            data.append(temp)
    folder  = r'{}'.format(data[0][:len(data[0])-1:])
    morning = r'{}'.format(data[1][:len(data[1])-1:])   #утро  (только англ.)
    day =     r'{}'.format(data[2][:len(data[2])-1:])   #день  (только англ.)
    evening = r'{}'.format(data[3][:len(data[3])-1:])   #вечер (только англ.)
    night =   r'{}'.format(data[4][:len(data[4])-1:])   #ночь  (только англ.)
    cooldown = int(r'{}'.format(data[5]))
    error = r"error.png"
    data.clear()
    config.close()

update()

def setWPchoosen(folder,wallpaper):
    full_path = os.path.join(folder, wallpaper)
    wp = bytes(full_path, 'utf-8')
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wp, 3)

    #Создание vbs скрипта, открывающего программу по смене обоев на экране блокировки в тихом режиме
    command = f'igcmdWin10.exe setlockimage {full_path}'
    subprocess.call(command)

missingFiles = ""

def isExist(folder, wallpaper):
    global missingFiles
    full_path = os.path.join(folder, wallpaper)
    if not(os.path.exists(full_path)):
        missingFiles += full_path + "\n"

def setWP():
    global missingFiles
    now = datetime.datetime.now()
    h = now.hour

    if    6 <= h < 12: wallpaper = morning
    elif 12 <= h < 18: wallpaper = day
    elif      h >= 18: wallpaper = evening
    elif        h < 6: wallpaper = night

    isExist(folder, morning)
    isExist(folder, day)
    isExist(folder, evening)
    isExist(folder, night)

    if len(missingFiles) > 0:
        setWPchoosen(folder,error)
        textOfError = "Check the correctness of the wallpaper names or folder path in the config.txt file:\n" + missingFiles
        missingFiles = ""

        hourStr   = str(now.hour)
        minuteStr = str(now.minute)
        secondStr = str(now.second)
        yearStr   = str(now.year)
        monthStr  = str(now.month)
        dayStr    = str(now.day)

        if now.hour   < 10: hourStr   = '0'+ hourStr
        if now.minute < 10: minuteStr = '0'+ minuteStr
        if now.second < 10: secondStr = '0'+ secondStr
        if now.month  < 10: monthStr  = '0'+ monthStr
        if now.day    < 10: dayStr    = '0'+ dayStr

        if not(os.path.exists("ErrorLogs")):
            os.mkdir("ErrorLogs")

        errorFile = open(f'ErrorLogs/Error {yearStr}-{monthStr}-{dayStr} {hourStr}-{minuteStr}-{secondStr}.txt','w')
        errorFile.write(textOfError)
        errorFile.close()
    else:
        setWPchoosen(folder,wallpaper)

setWP()

while True:
    if cooldown >= 1 and cooldown <= 59:
        print(cooldown)
        setWP()
        update()
        time.sleep(cooldown)
    else:
        now = datetime.datetime.now()
        h = now.hour
        if h % 6 == 0:
            update()