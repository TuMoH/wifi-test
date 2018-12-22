import argparse
import datetime
import os
import re
from subprocess import call
from subprocess import check_output
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def airport():
    return check_output("/System/Library/PrivateFrameworks/Apple*.framework/Versions/Current/Resources/airport -I | grep 'CtlRSSI\|CtlNoise\|lastTxRate\|maxRate'", shell=True)

def ping():
    return check_output("ping ya.ru -c 1 | grep 'icmp_seq=0 ttl='", shell=True)

def getTable():
    table = {}
    table['RSSI'] = 0
    table['Noise'] = 0
    table['lastTxRate'] = 0
    table['maxRate'] = 0
    table['ping'] = 0

    try:
        for line in airport().splitlines():
            pattern = re.compile('.*CtlRSSI:\s+(\-\d+).*')
            matcher = pattern.match(line)
            if matcher:
                table['RSSI'] = int(matcher.group(1))

            pattern = re.compile('.*CtlNoise:\s+(\-\d+).*')
            matcher = pattern.match(line)
            if matcher:
                table['Noise'] = int(matcher.group(1))

            pattern = re.compile('.*lastTxRate:\s+(\d+).*')
            matcher = pattern.match(line)
            if matcher:
                table['lastTxRate'] = int(matcher.group(1))

            pattern = re.compile('.*maxRate:\s+(\d+).*')
            matcher = pattern.match(line)
            if matcher:
                table['maxRate'] = int(matcher.group(1))
    except Exception:
        print('WTF WIFI???')

    try:
        for line in ping().splitlines():
                pattern = re.compile('.*time=(\d+)\.\d+ ms')
                matcher = pattern.match(line)
                if matcher:
                    table['ping'] = int(matcher.group(1))
                else: 
                    table['ping'] = 0
    except Exception:
        print('WTF PING???')

    return table


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    xs = []
    y_ping = []
    y_rssi = []
    y_noise = []
    y_rate = []
    y_max_rate = []

    def animate(i, xs, y_ping, y_rssi, y_noise, y_rate, y_max_rate):
        xs.append(i)

        table = getTable()
        print table

        y_rssi.append(table['RSSI'])
        y_noise.append(table['Noise'])
        y_rate.append(table['lastTxRate'])
        y_max_rate.append(table['maxRate'])
        y_ping.append(table['ping'])

        # xs = xs[-500:]
        # y_rssi = y_rssi[-500:]
        # y_noise = y_noise[-500:]
        # y_rate = y_rate[-500:]
        # y_max_rate = y_max_rate[-500:]
        # y_ping = y_ping[-500:]

        ax.clear()
        ax.plot(xs, y_rssi, color='m', label='rssi', linewidth=3)
        ax.plot(xs, y_noise, color='b', label='noise', linewidth=2)
        ax.plot(xs, y_rate, color='g', label='rate')
        ax.plot(xs, y_max_rate, color='y', label='max_rate')
        ax.plot(xs, y_ping, color='r', label='ping', linewidth=5)

        plt.grid(True)
        plt.legend()

    ani = animation.FuncAnimation(fig, animate, fargs=(xs, y_ping, y_rssi, y_noise, y_rate, y_max_rate), interval=1000)
    plt.show()
