#!/usr/bin/env python3
import HPMA115S0
import sys
import json
from sps30 import SPS30
import sht85
import time

def file_and_stdout(fp, str):
    fp.write("%s" %str)
    print(str, end='', flush=True)


def sps30_print_header(dev, label):
    """
    print sps30 device info
    """
    file_and_stdout(f, f"# SPS30 {label} Firmware version: {dev.firmware_version()}\n")
    file_and_stdout(f, f"# SPS30 {label} Product type: {dev.product_type()}\n")
    file_and_stdout(f, f"# SPS30 {label} Serial number: {dev.serial_number()}\n")
    file_and_stdout(f, f"# SPS30 {label} Status register: {dev.read_status_register()}\n")
    file_and_stdout(f,
        f"# Auto cleaning interval {label} : {dev.read_auto_cleaning_interval()}s\n")
    #file_and_stdout(f, f"# Set auto cleaning interval {label}: {dev.write_auto_cleaning_interval_days(2)}s\n")
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

        d[massa] = {}
        d[particle] = {}

        #print(label)
        #print(r)
        #print(label)
        m = r['sensor_data']['mass_density']
        for i in [ 'pm1.0', 'pm2.5']:
            d[massa][i] = f"{m[i]:.2f}"

        p = r['sensor_data']['particle_count']
        for i in [ 'pm0.5', 'pm1.0', 'pm2.5']:
            d[particle][i] = f"{p[i]:.2f}"

    return d


def sps30_print_data(fd, d, label):
    """
    print sps30 data
    """
    massa = f'{label}_m'
    particle = f'{label}_p'

    for i in [ 'pm1.0', 'pm2.5']:
        file_and_stdout(fd, f'{d[massa][i]:9};')

    for i in [ 'pm0.5', 'pm1.0', 'pm2.5']:
        file_and_stdout(fd, f'{d[particle][i]:9};')

def sht85_get_data():
    """
    get temperature and huminity
    """
    ## Temperature sensor
    #mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds 
    #rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW
    #print(f'serial number = {sht85.sn()}')
    #time.sleep(0.5e-3)

    d = {}
    t,rh = sht85.single_shot()
    #dp = sht85.dew_point(t,rh)
    d['t'] = f"{t:.2f}"
    d['rh'] = f"{rh:.2f}"

    return d


### MAIN

try:
    f = open("/home/pi/Bureaublad/meeting.csv", "w")

    print("Starting Honeywell: HPMA115S0")
    hpma115S0 = HPMA115S0.HPMA115S0("/dev/serial0")

    hpma115S0.init()
    hpma115S0.startParticleMeasurement()

    reference = SPS30(bus=1, logger='reference')
    sps30_print_header(reference, "reference")

    experiment = SPS30(3)
    sps30_print_header(experiment, "experiment")

    reference.start_measurement()
    experiment.start_measurement()

    file_and_stdout(f, "\n")
    file_and_stdout(f, "# count ; temp ; humidity ;")
    file_and_stdout(f, " hpma_2.5 ;")
    file_and_stdout(f, "rmass_1.0;  rmass_2.5; rpart_pm0.5; rpart_pm1.0; rpart_pm2.5;")
    file_and_stdout(f, "emass_1.0;  emass_2.5; epart_pm0.5; epart_pm1.0; epart_pm2.5;")
    file_and_stdout(f, "\n")

    file_and_stdout(f, "# number ; Celcius ; percentage ;")
    file_and_stdout(f, " ug/m3  ;")
    file_and_stdout(f, "ug/m3;  ug/m3; #/cm3; #/cm3; #/cm3;")
    file_and_stdout(f, "ug/m3;  ug/m3; #/cm3; #/cm3; #/cm3;")
    file_and_stdout(f, "\n")

    hpma = {} 
    c = 1
    file_and_stdout(f, "\n")
    while True:
        t_rh = sht85_get_data()

        h = hpma115S0.readParticleMeasurement()
        if (h):
            hpma['pm2.5'] = hpma115S0._pm2_5
        else:
            time.sleep(1)
            continue

        r = sps30_get_data(reference, "reference")
        e = sps30_get_data(experiment, "experiment")

        if (h and r and e and t_rh):
            file_and_stdout(f, f"{c:10};")
            file_and_stdout(f, f"{t_rh['t']:9}; {t_rh['rh']:9};");
            file_and_stdout(f, f"{hpma['pm2.5']:8};");
            sps30_print_data(f, r, "reference")
            sps30_print_data(f, e, "experiment")
            file_and_stdout(f, "\n")
            c += 1
        else:
            time.sleep(1)
            continue

        try:
            #f.write(f, f"{d['hpma115S0'][0]:8}; {d['sps30_m'][0]:9}; {d['sps30_m'][1]:9}; {d['sps30_p'][0]:9}; {d['sps30_p'][1]:9}; {d['sps30_p'][2]:9}\n")
            #file_and_stdout(f, f"{d['hpma115S0'][0]:8}; {d['sps30_m'][0]:9}; {d['sps30_m'][1]:9}; {d['sps30_p'][0]:9}; {d['sps30_p'][1]:9}; {d['sps30_p'][2]:9}")
            a=1 
        except IndexError:
            pass

        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping measurement...")
    reference.stop_measurement()
    experiment.stop_measurement()
    sht85.stop()
    sys.exit()
