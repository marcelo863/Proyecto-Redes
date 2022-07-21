import bluetooth
import random
import struct
from ble_advertising import advertising_payload
import sensor, image, time, os, tf

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_PERSON_CHAR = (
    bluetooth.UUID(0x2A6E),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_PERSON_CHAR,),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)


class BLEPerson:
    def __init__(self, ble, name="PORTENTA_BLE"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER
        )
        print("advertising...")
        self._advertise()


    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data


    def set_person(self, is_person, prob, notify=False, indicate=False):
        # Write the local value, ready for a central to read.

        prob = int(prob*1000)

        # codificación persona
        if is_person:
            data = prob + 10000
        else:
            data = prob

        self._ble.gatts_write(self._handle, struct.pack("<h", data))

        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)



def main():
    ble = bluetooth.BLE()
    person = BLEPerson(ble)

    # Configuración cámara
    sensor.reset()                         # Reset and initialize the sensor.
    sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
    sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
    sensor.set_windowing((240, 240))       # Set 240x240 window.
    sensor.skip_frames(time=2000)          # Let the camera adjust.

    # Load the built-in person detection network (the network is in your OpenMV Cam's firmware).
    labels, net = tf.load_builtin_model('person_detection')

    clock = time.clock()

    i = 0
    while True:
        clock.tick()

        # foto
        img = sensor.snapshot()

        # net.classify() will run the network on an roi in the image (or on the whole image if the roi is not
        # specified). A classification score output vector will be generated for each location. At each scale the
        # detection window is moved around in the ROI using x_overlap (0-1) and y_overlap (0-1) as a guide.
        # If you set the overlap to 0.5 then each detection window will overlap the previous one by 50%. Note
        # the computational work load goes WAY up the more overlap. Finally, for multi-scale matching after
        # sliding the network around in the x/y dimensions the detection window will shrink by scale_mul (0-1)
        # down to min_scale (0-1). For example, if scale_mul is 0.5 the detection window will shrink by 50%.
        # Note that at a lower scale there's even more area to search if x_overlap and y_overlap are small...

        # default settings just do one detection... change them to search the image...
        for obj in net.classify(img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):

            print("**********\nDetalles de reconocimiento")

            for i in range(len(obj.output())):
                print("%s = %f" % (labels[i], obj.output()[i]))

            # si es persona o no
            max_label = labels[obj.output().index(max(obj.output()))]
            prob_no_person, prob_person = obj.output()

            if prob_person > 0.6:
                print("Persona detectada!")

                # person.set_person(1, False, notify=True, indicate=False)
                person.set_person(1, prob_person, notify=True, indicate=False)
            else:
                # person.set_person(0, False, notify=True, indicate=False)
                person.set_person(0, prob_no_person, notify=True, indicate=False)

            img.draw_rectangle(obj.rect())
            img.draw_string(obj.x()+3, obj.y()-1, max_label, mono_space = False)

        print(clock.fps(), "fps")

        time.sleep_ms(2000)


main()
