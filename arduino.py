import serial

class Arduino(object):

    def __init__(self, port='/dev/cu.usbmodem1411', baudrate=9600):
        self.serial = serial.Serial(port, baudrate)
        self.serial.write(b'99')

    def __str__(self):
        return "Arduino is on port %s at %d baudrate" % (self.serial.port, self.serial.baudrate)

    def stopMotor(self):
        self.__sendData('1')

    def backwardMotor(self):
        self.__sendData('2')

    def forwardMotor(self):
        self.__sendData('3')

    def getMotor(self):
        self.__sendData('4')
        return self.__getData()

    def getHammer(self):
        self.__sendData('5')
        v1 = self.__getData()
        v2 = self.__getData()
        v3 = self.__getData()
        v4 = self.__getData()
        v5 = self.__getData()
        return (int(v1), int(v2), int(v3), int(v4), int(v5))

    def __sendData(self, serial_data):
        while(self.__getData()[0] != "w"):
            pass
        #print '__sendData', serial_data
        serial_data = str(serial_data).encode('utf-8')
        self.serial.write(serial_data)

    def __getData(self):
        input_string = self.serial.readline()
        input_string = input_string.decode('utf-8')
        #print '__getData', input_string
        return input_string.rstrip('\n')

    def close(self):
        self.serial.close()
        return True
