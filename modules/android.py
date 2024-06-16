
def devdec():
    from device_detector import DeviceDetector
    from device_detector import SoftwareDetector
    import platform
    import kivy
    import pynput

    print('in android module...')
    ua = platform.platform()
    # Parse UA string and load data to dict of 'os', 'client', 'device' keys
    device = DeviceDetector(ua).parse()

    # Use helper methods to extract data by attribute

    print(device.is_bot())      # >>> False
    ua = platform.system()
    device = SoftwareDetector(ua).parse()

    print('Client Name:', device.client_name())        # >>> Chrome Mobile
    #device.client_short_name()  # >>> CM
    print(device.client_type())        # >>> browser
    print(device.client_version())     # >>> 58.0.3029.83

    print('Device os Name:', device.os_name())     # >>> Android
    print('Device os Version:', device.os_version())  # >>> 6.0
    print('Device Engine:', device.engine())      # >>> WebKit

    #device.device_brand_name()  # >>> ''
    print('Device Brand:', device.device_brand()) # >>> ''
    print('Device Model:', device.device_model())       # >>> ''
    print('device type is:', device.device_type())  # >>> ''
    print('poka:', kivy.platform)
    print(kivy.environ)
    print(pynput.keyboard.Events)
    import pygetwindow
    print(pygetwindow.getActiveWindow())
    print(pygetwindow.getAllTitles())

devdec()