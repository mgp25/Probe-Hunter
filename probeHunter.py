import re, os, sys, signal, threading, time, subprocess, argparse, itertools
from wigle import Wigle
from subprocess import Popen, PIPE
from colorclass import Color
from terminaltables import AsciiTable

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161]

parser = argparse.ArgumentParser()
parser.add_argument("--iface", help='Interface to capture data', required=True)
args = parser.parse_args()

run = True
wigle_flag = False
if Wigle.AUTH == '':
    wigle_flag = True

def signal_handler(sig, frame):
    global run
    run = False
    print('Bye! ;)')
    print('Exiting, please wait...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def print_data():
    while run:
        table = AsciiTable(sorted(data, key=lambda x: x[3]))
        os.system("clear")
        print(table.table+"\n\n")
        time.sleep(2)

def check_vendor(mac):
    with open('macvendors.txt', 'r') as f:
        for line in f:
            l = line.split('\t')
            if l[0].lower() in mac.replace(':', '') :
                return l[1].strip()
    return '-'

def signal_power(signal):
    if signal <= -70:
        return Color("{autored}"+str(signal)+"{/autored}")
    elif signal > -70 and signal < -55:
        return Color("{autoyellow}"+str(signal)+"{/autoyellow}")
    else:
        return Color("{autogreen}"+str(signal)+"{/autogreen}")

def hop_channel_mac():
    for channel in itertools.cycle(channels):
        if run == False:
            break
        try:
            subprocess.run(["sudo", "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-c"+str(channel)])
        except Exception as e:
            pass
        time.sleep(3)

def hop_channel_linux():
    for channel in itertools.cycle(channels):
        if run == False:
            break
        try:
            subprocess.run(["sudo", "iwconfig" ,args.iface, "channel", channel])
        except Exception as e:
            pass
        time.sleep(3)

data = []
registered = {}
data.append([Color("{autogreen}Freq. (MHz){/autogreen}"), Color("{autogreen}Pow. (dBm){/autogreen}"), Color("{autogreen}MAC{/autogreen}"), Color("{autogreen}SSID{/autogreen}"), Color("{autogreen}Vendor{/autogreen}"), Color("{autogreen}Coords. (Lat-Long){/autogreen}")])

if sys.platform == "darwin":
    subprocess.run(["sudo", "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-z"])
    process = Popen('tcpdump -l -I -i '+args.iface+' -e -s 256 type mgt subtype probe-req', bufsize=1, universal_newlines=True,
                    shell=True, stdout=PIPE, stderr=PIPE)
    threading.Thread(target=hop_channel_mac).start()
elif sys.platform == "linux":
    subprocess.run(["ifconfig", args.iface, "down"])
    subprocess.run(["iwconfig", args.iface, "mode", "monitor"])
    subprocess.run(["ifconfig", args.iface, "up"])
    process = Popen(["/usr/sbin/tcpdump", "-i", args.iface, "-e", "-s", "256", "type mgt subtype probe-req"], bufsize=1, universal_newlines=True,
                    stdout=PIPE, stderr=PIPE)
    threading.Thread(target=hop_channel_linux).start()

threading.Thread(target=print_data).start()
for row in iter(process.stdout.readline, b''):
    groups = re.search(".* Mb\/s (\d+) .* (-\d+)dBm signal .* SA:(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}) .* Probe \w+ \(([^\)]+)\)", row.strip())
    if groups != None:
        signal = signal_power(int(groups.group(2)))
        if not groups.group(4) in registered:
            registered[groups.group(4)] = []
        if not groups.group(3) in registered[groups.group(4)]:
            registered[groups.group(4)].append(groups.group(3))
            company = check_vendor(groups.group(3))
            wigle = Wigle.wigle_location(groups.group(4), wigle_flag)
            if wigle == 1:
                wigle_flag = True
            if wigle is 2 and not wigle_flag:
                loc = '-'
            elif wigle is None and not wigle_flag:
                loc = '?+'
            elif wigle_flag:
                loc = 'Disabled'
            else:
                loc = str(wigle['trilat'])+', '+str(wigle['trilong'])

            data.append([groups.group(1), signal, groups.group(3), groups.group(4), company, loc])
        elif groups.group(3) in registered[groups.group(4)]:
            for sublist in data:
                if groups.group(3) in sublist:
                    sublist[1] = signal
