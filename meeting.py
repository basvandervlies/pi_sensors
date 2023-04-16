#!/usr/bin/env python3
import HPMA115S0
import sys
import json
from sps30 import SPS30
import time

def file_and_stdout(fp, str):
    fp.write("%s\n" %str)
    print(str)


def sps30_print_header(dev, label):
    """
    print sps30 device info
    """
    file_and_stdout(f, f"# SPS30 {label} Firmware version: {dev.firmware_version()}")
    file_and_stdout(f, f"# SPS30 {label} Product type: {dev.product_type()}")
    file_and_stdout(f, f"# SPS30 {label} Serial number: {dev.serial_number()}")
    file_and_stdout(f, f"# SPS30 {label} Status register: {dev.read_status_register()}")
    file_and_stdout(f,
        f"# Auto cleaning interval {label} : {dev.read_auto_cleaning_interval()}s")
    #file_and_stdout(f, f"# Set auto cleaning interval {label}: {dev.write_auto_cleaning_interval_days(2)}s")
    file_and_stdout(f, f"# {label} End\n ")

def sps30_get_data(dev, label):
    """
    get a reading from SPS30 device
    """
    d = {}
    massa = f'{label}_m'
    particle = f'{label}_p'

    r = dev.get_measurement()
    if (r):

        d[massa] = []
        d[particle] = []

        print(label)
        print(r)
        print(label)
        m = r['sensor_data']['mass_density']
        d[massa].append(m['pm2.5'])
        d[massa].append(m['pm1.0'])

        p = r['sensor_data']['particle_count']
        d[particle].append(p['pm2.5'])
        d[particle].append(p['pm1.0'])
        d[particle].append(p['pm0.5'])

    return d

try:
    f = open("/home/pi/Bureaublad/meeting.csv", "w")

    print("Starting Honeywell: HPMA115S0")
    hpma115S0 = HPMA115S0.HPMA115S0("/dev/serial0")

    hpma115S0.init()
    hpma115S0.startParticleMeasurement()

    reference = SPS30(bus=1, logger='reference')
    sps30_print_header(reference, "reference")

    #time.sleep(2)

    measure = SPS30(3)
    sps30_print_header(measure, "measure")

    reference.start_measurement()
    measure.start_measurement()



    d = {}
    d['hpma115S0'] = []
    d['sps30_m'] = []
    d['sps30_p'] = []

    file_and_stdout(f, "# hpma_2.5 mass_2.5 mass_1.0 part_pm2.5 part_pm1.0 part_pm0.5")
    file_and_stdout(f, "#          ug/m3                        #/cm3")   

    while True:
        r = hpma115S0.readParticleMeasurement()
        if (r):
            d['hpma115S0'].append(hpma115S0._pm2_5)

        r = sps30_get_data(reference, "reference")
        if (r):
            print(r)
        else:
            time.sleep(1)
            continue

        r = sps30_get_data(measure, "measure")
        if (r):
            print(r)
        else:
            time.sleep(1)
            continue

        sys.exit(0)

        try:
            #f.write(f, f"{d['hpma115S0'][0]:8}; {d['sps30_m'][0]:9}; {d['sps30_m'][1]:9}; {d['sps30_p'][0]:9}; {d['sps30_p'][1]:9}; {d['sps30_p'][2]:9}\n")
            file_and_stdout(f, f"{d['hpma115S0'][0]:8}; {d['sps30_m'][0]:9}; {d['sps30_m'][1]:9}; {d['sps30_p'][0]:9}; {d['sps30_p'][1]:9}; {d['sps30_p'][2]:9}")
        except IndexError:
            pass

        d['hpma115S0'] = []
        d['sps30_m'] = []
        d['sps30_p'] = []
        
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping measurement...")
    sps30.stop_measurement()
    sys.exit()
