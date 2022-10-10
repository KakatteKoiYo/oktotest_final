import RPi.GPIO as GPIO
import time, serial, requests
from binascii import unhexlify, hexlify

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


#GPIO.cleanup()
def getSerialFromMC(event = ""):
    serialPort = serial.Serial(port = "/dev/serial0", baudrate = 1200, timeout = 1)
    serialPort.flushInput()
    serialPort.flushOutput()
    serialPort.flush()
    #Comando para obtener serial de micro U7 
    comando = "2586F90458"
    serialPort.write(unhexlify(comando))
    respuestaBytes = serialPort.read(size = 10)
    respuestaHex = hexlify(respuestaBytes).decode().upper()
    serialHex = respuestaHex.split(comando)[1][:8]
    if len(respuestaHex) > 15:
        AclaraFormato = ""
        for i in range(len(serialHex)):
            if i != 0 and i%2 == 0:
                AclaraFormato += " "+serialHex[i].upper()
            else:
                AclaraFormato += serialHex[i].upper()

        ArrayHex = AclaraFormato.split(" ")[::-1]
        reversedHex = ""
        for i in ArrayHex:
            reversedHex += i
        serialDec = int(reversedHex, 16)
        print(serialDec)
    else:
        print("No hubo respuesta...")
    serialPort.close()
    

GPIO.add_event_detect(17, GPIO.RISING, bouncetime = 1000, callback = getSerialFromMC)

try:
    while True:
        time.sleep(0.2)
except:
    GPIO.cleanup()