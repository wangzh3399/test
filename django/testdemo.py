from monitorStrategy import *
import time
import datetime
from basicfunc import *
import traceback

timestampList = ['16807106','16807446','16807452','16807458','16807464','16807470','16807476','16807482','16807488']   #16807446  9.30  

#timelist = ['0915','0920','0925','0920','0925','0920','0925','0920','0925','0920','0925','0920','0925','0920','0925',]

if __name__ == '__main__':
    logger = getlogger('testinterface.log')
    logger.info("start!!!")
    monitorObj = monitorStrategy()
    while True:
        t = datetime.datetime.now()
        #hour = ('0'+str(t.hour))
        #hour = hour[len(hour)-2:]

        #minute = '0'+str(t.minute)
        #minute = minute[len(minute)-2:]
        minute = t.minute
        #timestr = hour+minute
        #print(timestr)
        #timestamp = str(t.timestamp()).split('.')[0][0:8]
        #if timestamp in  timestampList:
        if minute%5==0:
            #timestampList.remove(timestamp)
            #timestr.remove(timestr)
            try:
                monitorObj.testEmInterface()
            except:
                logger.error(traceback.format_exc())
            try:
                monitorObj.testSinaInterface()
            except:
                logger.error(traceback.format_exc())
            time.sleep(60)
        else:
            logger.info("do sleep 30s!!!")
            time.sleep(10)
            logger.info("sleep over!!!")
