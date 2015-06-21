import math
import numpy
import pyaudio
import json
import time
import serial
import sys


def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=440, length=1, rate=44100):
    chunks = []
    chunks.append(sine(frequency, length, rate))

    chunk = numpy.concatenate(chunks) * 0.25

    stream.write(chunk.astype(numpy.float32).tostring())

def leeRgb(colorRgb):
    parentesis1 = colorRgb.find("(")+1
    parentesis2 = colorRgb.find(")")
    colorRgb = colorRgb[parentesis1:parentesis2]
    colorestxt = colorRgb.split(",")
    colores = [int(x) for x in colorestxt]
    R = colores[0]
    G = colores[1]
    B = colores[2]
    return (R,G,B)


def preparasincro():
    sincro = open("sincroniza","w")
    sincro.write("0")
    sincro.close()

def esperasincro():
    desincronizado = 0
    while desincronizado == 0:
        sincro = open("sincroniza","r")
        try:
            desincronizado = int(sincro.read())
        except:
            desincronizado = 0
        sincro.close()
        time.sleep(0.02)

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)
    ser = serial.Serial("/dev/ttyUSB0",9600)
    preparasincro()
    #esperasincro()
    indice = 0
    cuantos = 48300
    t = numpy.linspace(2*numpy.pi/44100,2*cuantos*numpy.pi/44100,cuantos)
    while True:
        secuenciafile = open("secuencia.json","r")
        secuencia = json.load(secuenciafile)
        secuenciafile.close()
        colorRgb = secuencia[indice]["color"]
        frecuencias = secuencia[indice]["frecuencias"]
        y = numpy.zeros(cuantos)
        suave = numpy.sin(0.5*t)
        for frec in frecuencias:
            tono = numpy.sin(frec*t)
            y+=tono
        y=y*suave*9.0
        if indice == 0:
            preparasincro()
            esperasincro()
        stream.write(y.astype(numpy.float32))
        R,G,B = leeRgb(colorRgb)
        cadenita = ",".join([str(R),str(G),str(B)])+","
        #cadenita = "255,255,255,0,0,0"+","
        ser.write(cadenita)
        #print cadenita,
        indice =(indice + 1)%16

    #play_tone(stream)

    #stream.close()
    #p.terminate()
