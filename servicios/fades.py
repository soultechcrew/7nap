import math
import numpy
import json
import time
import serial


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
    ser = serial.Serial("/dev/ttyUSB0",9600)
    indice = 0
    secuenciafile = open("bosque.json","r")
    secuencia = json.load(secuenciafile)
    secuenciafile.close()
    while True:
        colorRgb = secuencia[indice]
        R1,G1,B1 = leeRgb(colorRgb)
        indice2 = (indice+1)%5
        colorRgb2 = secuencia[indice2]
        R2,G2,B2 = leeRgb(colorRgb2)
        Rs = [int(x) for x in numpy.round(numpy.linspace(R1,R2,60))]
        Gs = [int(x) for x in numpy.round(numpy.linspace(G1,G2,60))]
        Bs = [int(x) for x in numpy.round(numpy.linspace(B1,B2,60))]
        for i in range(0,60):
            R,G,B = Rs[i],Gs[i],Bs[i]
            cadenita = ",".join([str(R),str(G),str(B),str(255-R),str(255-G),str(255-B)])+","
            ser.write(cadenita)
            #time.sleep(.005)
            print R,G,B
        indice =(indice + 1)%5

    #play_tone(stream)

    #stream.close()
    #p.terminate()
