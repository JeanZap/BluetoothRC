import time
from machine import PWM, Pin, UART
import json

MIN_DUTY = 1700
MAX_DUTY = 8200

pinoServo = 15
servoPwm = PWM(Pin(pinoServo))
servoPwm.freq(50)

pinoMotor = 14
motorPwm = PWM(Pin(pinoMotor))
motorPwm.freq(50)

bluetoothModule = UART(0, 9600)

def definirValoresIniciais():
    ledImbutido = 25

    Pin(ledImbutido).low()
    servoPwm.duty_u16(obterDutyDirecao(90))

def obterDutyDirecao(direcao):
    intervaloPorGrau = (MAX_DUTY - MIN_DUTY) / 180
    return int(intervaloPorGrau * direcao) + MIN_DUTY

def obterDutyMotor(velocidade):
    intervaloPorGrau = (MAX_DUTY - MIN_DUTY) / 180
    return int(intervaloPorGrau * velocidade) + MIN_DUTY

def tratarDadosBluetooth(dados):
    return str(dados).replace('\\', '').replace("b'{", "{").replace("}'", '}')

def obterDadoBluetooth():
    dadosObtidos = bluetoothModule.read()
    dadosObtidos = tratarDadosBluetooth(dadosObtidos)
    return json.loads(dadosObtidos)

definirValoresIniciais()
while True:
    if bluetoothModule.any():
        try:
            command = obterDadoBluetooth()
            servoPwm.duty_u16(obterDutyDirecao(command['direcao']))
            motorPwm.duty_u16(obterDutyMotor(command['velocidade']))
        except:
            pass
