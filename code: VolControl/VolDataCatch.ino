#define ptMeter 0

float lecturaFiltrada = 0;

float convertirA100(int valor) {
    valor = constrain(valor, 1, 3330);
    return 1.0 + (valor - 1) * (99.0 / 3329.0);
}

void setup() {
    Serial.begin(115200);
    analogReadResolution(12);
}

void loop() {
    int lectura = analogRead(ptMeter);

    // Filtro exponencial
    lecturaFiltrada = 0.6 * lecturaFiltrada + 0.4 * lectura;

int porcentaje = (int)convertirA100((int)lecturaFiltrada);

static int ultimo = -1;
if (porcentaje != ultimo) {
    Serial.println(porcentaje);
    ultimo = porcentaje;
Serial.println((int)porcentaje);
delay(20);
}
}
