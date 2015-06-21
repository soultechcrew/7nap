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


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)
    ser = serial.Serial("/dev/ttyUSB0",9600)
    indice = 0
    while True:
        secuenciafile = open("secuencia.json","r")
        secuencia = json.load(secuenciafile)
        secuenciafile.close()
        colorRgb = secuencia[indice]["color"]
        frecuencias = secuencia[indice]["frecuencias"]
        t = numpy.linspace(2*numpy.pi/44100,2*numpy.pi,44100)
        y = numpy.zeros(44100)
        suave = numpy.sin(0.5*t)
        for frec in frecuencias:
            tono = numpy.sin(frec*t)
            y+=tono
        y=y*suave*9.0
        stream.write(y.astype(numpy.float32))
        R,G,B = leeRgb(colorRgb)
        cadenita = ",".join([str(R),str(G),str(B),str(255-R),str(255-G),str(255-B)])+","
        #cadenita = "255,255,255,0,0,0"+","
        ser.write(cadenita)
        #print cadenita,
        time.sleep(.10)
        indice =(indice + 1)%16

    #play_tone(stream)

    #stream.close()
    #p.terminate()
