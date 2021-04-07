import sys
import pytz
from datetime import datetime, timezone, timedelta
import urllib.request
import xml.etree.ElementTree as ET

if __name__ == '__main__':

    ate = datetime.now()

    if len(sys.argv) == 2:
        de = datetime.strptime(sys.argv[1], "%d/%m/%Y %H:%M:%S")
        #aero = 'SBPA'   # aeroporto Salgado Filho (Porto Alegre)
        aero = 'SBCO'   # aeroporto Canoas
    elif len(sys.argv) == 3:
        de = datetime.strptime(sys.argv[1], "%d/%m/%Y %H:%M:%S")
        aero = sys.argv[2]
    elif len(sys.argv) == 4:
        de = datetime.strptime(sys.argv[1], "%d/%m/%Y %H:%M:%S")
        ate = datetime.strptime(sys.argv[2], "%d/%m/%Y %H:%M:%S")
        aero = sys.argv[3] 
    else:
        de = ate - timedelta(days=1)
        aero = 'SBCO'   # aeroporto Canoas

    deutc = de.astimezone(timezone.utc)
    ateutc = ate.astimezone(timezone.utc)

    link='https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&startTime=' + \
        deutc.strftime("%Y-%m-%dT%H:%M:%SZ") + '&endTime=' + ateutc.strftime("%Y-%m-%dT%H:%M:%SZ") + '&stationString=' + aero

    print(link, '\n\n')

    webUrl = urllib.request.urlopen(link)
    data = webUrl.read()
    #print("data:", data)

    root = ET.fromstring(data)

    #f = open('xml.txt', 'w')
    #f.write(ET.canonicalize(ET.tostring(root)))
    #f.close()

    for metars in reversed(root.find('data').findall('METAR')):
        dt = datetime.strptime(metars.find('observation_time').text, "%Y-%m-%dT%H:%M:%S%z").astimezone(pytz.timezone('America/Sao_Paulo'))
        t = float(metars.find('temp_c').text)
        to = float(metars.find('dewpoint_c').text)
        p = float(metars.find('altim_in_hg').text)
        pmb = p * 0.0338639 * 1000
        u = 100 - 5 * (t - to)

        print('local: ', aero, ' data e hora: ', dt, " temperatura: %2.0f︒C" % t, " ponto de orvalho: %2.0f︒C" % to, " (umidade: %5.1f%%" % u, ") pressão: %5.2f" % \
            p, ' inHg (%6.1f mb)' % pmb, sep='')

    