#!/usr/bin/env python3
import HPMA115S0
import sys
import json
from sps30 import SPS30
import time

def file_and_stdout(fp, str):
    fp.write("%s\n" %str)
    print(str)

try:
    f = open("/home/pi/Bureaublad/meeting.csv", "w")

    print("Starting Honeywell: HPMA115S0")
    hpma115S0 = HPMA115S0.HPMA115S0("/dev/serial0")

    hpma115S0.init()
    hpma115S0.startParticleMeasurement()

    sps30 = SPS30()
    file_and_stdout(f, f"# SPS30 Firmware version: {sps30.firmware_version()}")
    file_and_stdout(f, f"# SPS30 Product type: {sps30.product_type()}")
    #file_and_stdout(f, f"# SPS30 Serial number: {sps30.serial_number()}")
    file_and_stdout(f, f"# SPS30 Status register: {sps30.read_status_register()}")
    file_and_stdout(f,
        f"# Auto cleaning interval: {sps30.read_auto_cleaning_interval()}s")
    file_and_stdout(f, f"# Set auto cleaning interval: {sps30.write_auto_cleaning_interval_days(2)}s")
    sps30.start_measurement()

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

        r = sps30.get_measurement()
        if (r):
            print(r)
            m = r['sensor_data']['mass_density']
            d['sps30_m'].append(m['pm2.5'])
            d['sps30_m'].append(m['pm1.0'])

            p = r['sensor_data']['particle_count']
            d['sps30_p'].append(p['pm2.5'])
            d['sps30_p'].append(p['pm1.0'])
            d['sps30_p'].append(p['pm0.5'])
        else:
            time.sleep(1)
            continue

        try:
            #f.write(f, f"{d['hpma115S0'][0]:8}; {d['sps30_m'][0]:9}; {d['sps30_m'][1]:9}; {d['sps30_p'][0]:9}; {d['sps30_p'][1]:9}; {d['sps30_p'][2]:9}\n")
            file_and_stdout(f, f"{d['hpma115S0'][0]:8}; {d['sps30_m'][0]:9}; {d['sps30_m'][1]:9}; {d['sps30_p'][0]:9}; {d['sps30_p'][1]:9}; {d['sps30_p'][2]:9}")
        except IndexError:
            pass

        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping measurement...")
    sps30.stop_measurement()
    sys.exit()
