#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import datetime

str2date = lambda x: datetime.datetime.strptime(x.decode("utf-8"), '%Y-%m-%d')


# skip_header=4 to ship the CSV header and the first 3 data rows 
# which are anomalous
data = numpy.genfromtxt('latencies.csv', delimiter=',', skip_header=4, 
    names='day,count,mean,std,min,25%,50%,75%,90%,99%,max', dtype=None,
    converters={0: str2date})

plt.figure(1, figsize=(7.0,10.0))

plt.suptitle('SIRI data feed - volume and delay')

plt.subplot(611)
plt.grid()
plt.plot(data['day'], data['count'], linestyle='-', marker='.', markersize=4)
plt.ylabel('Vehicle journeys')

plt.subplot(612)
plt.grid()
plt.plot(data['day'],data['mean'])
plt.legend(['Mean', 'SD'], loc=2)
plt.ylabel('Delay (seconds)')

plt.subplot(613)
plt.grid()
plt.plot(data['day'], data['min'])
plt.legend(['Min'], loc=2)
plt.ylabel('Delay (seconds)')

plt.subplot(614)
plt.grid()
plt.plot(data['day'], data['25'])
plt.plot(data['day'], data['50'])
plt.legend(['25%', '50%'], loc=2)
plt.ylabel('Delay (seconds)')

plt.subplot(615)
plt.grid()
plt.plot(data['day'], data['99']/60)
plt.legend(['99%',], loc=2)
plt.ylabel('Delay (minutes)')

plt.subplot(616)
plt.grid()
plt.plot(data['day'], data['max']/60)
plt.legend(['Max'], loc=2)
plt.ylabel('Delay (minutes)')

plt.savefig('siri_analysis')
