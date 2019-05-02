# -*- coding: utf-8 -*-
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import MySQLdb
import datetime

Broker = "127.0.0.1"
db = MySQLdb.connect("localhost", "root", "monitoreo", "monitoreo")
c=db.cursor()

vac = 0
iac = 0
wac = 0
ipanel = 0
vpanel = 0
wpanel = 0
iaero = 0
vaero = 0
waero = 0
tpanel = 0
rad = 0
lux = 0
temp_int = 0
temp_ext = 0
hum_int = 0
hum_ext = 0
tbat = 0
vbat = 0
tpanel = 0
i_panel = 0
dew = 0
rad_comp = 1
isc = 0
T = 0

flag_1 = 1
muestra_min = 10


def on_connect(client, userdata, flags, rc):
    #print("Conected with result code " +str(rc))
    client.subscribe("#")
    

def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    #print(msg.topic+"  "+message)
    global vac, iac, wac, vpanel, ipanel, wpanel, vaero, iaero, waero, vbat, tbat, temp_int, temp_ext, hum_int, hum_ext, rad, tpanel, i_panel, lux, dew, isc ,T
    tema = msg.topic
    if str(tema) == "vac": 
        vac = str(msg.payload.decode("utf-8"))
    if str(tema) == "iac": 
        iac = str(float(msg.payload.decode("utf-8")) * 1000)
    if str(tema) == "wac": 
        wac = str(msg.payload.decode("utf-8"))
    if str(tema) == "vpanel": 
        vpanel = str(msg.payload.decode("utf-8"))
    if str(tema) == "ipanel": 
        ipanel = str(msg.payload.decode("utf-8"))    
    if str(tema) == "wpanel": 
        wpanel = str(msg.payload.decode("utf-8"))
    if str(tema) == "vaero": 
        vaero = str(msg.payload.decode("utf-8"))
    if str(tema) == "iaero": 
        iaero = str(msg.payload.decode("utf-8"))   
    if str(tema) == "waero": 
        waero = str(msg.payload.decode("utf-8"))

    if str(tema) == "vbat": 
        vbat = str(msg.payload.decode("utf-8"))
    if str(tema) == "tbat": 
        tbat= str(msg.payload.decode("utf-8"))

    if str(tema) == "/esp2/temp": 
        temp_int = str(msg.payload.decode("utf-8"))
    if str(tema) == "/esp3/temp": 
        temp_ext = str(msg.payload.decode("utf-8"))

    if str(tema) == "/esp2/hum": 
        hum_int = str(msg.payload.decode("utf-8"))
    if str(tema) == "/esp3/hum": 
        hum_ext = str(msg.payload.decode("utf-8"))   
    if str(tema) == "/esp3/ipanel": 
        i_panel = str(float(msg.payload.decode("utf-8")) * 1000)
        isc = float(msg.payload.decode("utf-8"))
        last = time.strftime("%Y-%m-%d %H:%M")
        print("esp3")
        print(last)
        #print(i_panel)
    if str(tema) == "tpanel": 
        tpanel = str(msg.payload.decode("utf-8"))
        T = float(msg.payload.decode("utf-8"))
        #print(tpanel)
    if str(tema) == "rad1": 
        rad = str(float(msg.payload.decode("utf-8")) * 1000)
        #print(rad)
    if str(tema) == "lux": 
        lux = str(msg.payload.decode("utf-8"))
         
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883 ,60)
client.loop_start()

#print ("\nfecha    hora      temperatura    humedad   voltaje   vac")
#print ("=============================================================")  

while True:
    #global flag_1
    if (((int(time.strftime("%M")) % muestra_min) == 0) or (int(time.strftime("%M")) == 0)) and (flag_1 == 1):
        print("Enviando señal broadcast")
        publish.single("database", "Z", hostname="127.0.0.1")
        fecha = time.strftime("%Y-%m-%d %H:%M")
        time.sleep(8)
        rad_comp = round(abs(((isc-(0.025*(T-25))/0.64)*1000)), 2)
        #print(rad_comp)
        c.execute("INSERT INTO sistema (fecha, vac, iac, wac, vpanel, ipanel, wpanel, vaero, iaero, waero, temp_int, temp_ext, hum_int, hum_ext, vbat, tbat, lux, tpanel, i_panel, rad, rad_comp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(fecha, vac, iac, wac, vpanel, ipanel, wpanel, vaero, iaero, waero, temp_int, temp_ext, hum_int, hum_ext, vbat, tbat, lux, tpanel, i_panel, rad, rad_comp))
        db.commit()
        flag_1 = 0
        print(fecha)
        print("muestra tomada")
        #print(flag_1)
    else:
        if ((int(time.strftime("%M")) % muestra_min) != 0):
            flag_1 = 1
            #print(flag_1)
            #print((int(time.strftime("%M")) % muestra_min))
        else:
            time.sleep(1)
    #for reading in c.fetchall():
    #    c.execute ("SELECT * FROM monitoreo")
    # 0   print (str(reading[0])+"	"+str(reading[1])+"	"+str(reading[2])+"	"+str(reading[3])+"	"+str(reading[4])+"	"+str(reading[5]))
    

