import smbus
import time

bus = smbus.SMBus(1)


IODIRA = 0x00
IODIRB = 0x10
GPIOA = 0x12
OLATA = 0x14
GPPUA = 0x0C
bus.write_byte_data(0x21, IODIRA, 0x00)
bus.write_byte_data(0x21, GPPUA, 0xFF)



while True:
    bus.write_byte_data(0x21, OLATA, 0x04)
    a = bus.read_byte_data(0x21, GPIOA)
    print(a)
    time.sleep(0.5)
    bus.write_byte_data(0x21, OLATA, 0x02)
    a = bus.read_byte_data(0x21, GPIOA)
    print(a)
    time.sleep(0.5)


    