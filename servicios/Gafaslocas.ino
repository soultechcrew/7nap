         const int sensorPin = A1;    // pin that the sensor is attached to
	 const int pinLedR  = 5;
	 const int pinLedV  = 7;
	 const int pinLedA  =  6;
          const int pinLedR1  = 12;
	 const int pinLedV1  = 13;
	 const int pinLedA1  =  11;

	 // Variables para guardar el brillo de cada color
        int sensorValue = 0;         // the sensor value
        int sensorMin = 1023;        // minimum sensor value
        int sensorMax = 0;           // maximum sensor value
	 int brilloR = 0;
	 int brilloV = 0;
	 int brilloA = 0;

	 // Constante para controlar la pausa entre cambios
	 const int pausa = 1;

	 // Constante con la magnitud del cambio en el brillo

	 const int cambio = 5;

	 // Funcion que pone el brillo a los colores del led RGB 
	 void colorLed(int brilloRojo, int brilloVerde, int brilloAzul) {
	     analogWrite(pinLedR, brilloRojo);
	     analogWrite(pinLedV, brilloVerde);
	     analogWrite(pinLedA, brilloAzul);
	   } 
            void colorLed1(int brilloRojo1, int brilloVerde1, int brilloAzul1) {
              analogWrite(pinLedR1, brilloRojo1);
	     analogWrite(pinLedV1, brilloVerde1);
	     analogWrite(pinLedA1, brilloAzul1);
}

	 void setup() {
	     // Inicia y configura la comunicacion serial
	     Serial.begin(9600);
	     // Envia un mensaje con las instrucciones
	     Serial.println("Envia los valores entre 0-255 R,G,B,R1,G1,B1");
	     Serial.println("R,G,B ascendente ");
	     Serial.println("R1,G1,B1 descendente");

            pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);


  // signal the end of the calibration period
  digitalWrite(13, LOW);
  colorLed(0, 0, 0);
  colorLed1(255, 255, 255);
              
}

	 

	 void loop() {
	     if (Serial.available()) {
	         int  brilloR= Serial.parseInt();
                 int  brilloV= Serial.parseInt();
                  int  brilloA= Serial.parseInt();
                   int  brilloR1= Serial.parseInt();
                 int  brilloV1= Serial.parseInt();
                  int  brilloA1= Serial.parseInt();
                  char basura = Serial.read();

             


	         colorLed(brilloR, brilloV, brilloA);
                 colorLed1(brilloR1, brilloV1, brilloA1);
                 delay(pausa);
              }
         }
    
