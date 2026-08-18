"""
Example Description:
    This example shows how to poll the 4042E remote power monitor/sensor
    for forward power, reflected power, and VSWR information.

@verbatim

The MIT License (MIT)

Copyright (c) 2024 Bird

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@endverbatim

Copyright (c) Bird

"""
from bird_4042e import Bird4042E_Sensor
import time

mysensor = Bird4042E_Sensor("192.168.3.200")    #192.168.3.200   #10.128.0.174

print(f"Model: {mysensor.get_model()}")

#mysensor.get_channel_count()

channel_count = mysensor.get_channel_count()

for j in range(1, channel_count+1):   
    print(f"Name: {mysensor.get_channel_name(channel=j)}")

reserved = mysensor.get_channel_name(channel=1)

mysensor.set_channel_name(channel=1, name="CH_01")
print(f"Name: {mysensor.get_channel_name(channel=1)}")

mysensor.set_channel_name(channel=1, name=reserved)
print(f"Name: {mysensor.get_channel_name(channel=1)}")

mysensor.add_channel()
channel_count = mysensor.get_channel_count()
# set the name
mysensor.set_channel_name(channel=channel_count, name="Golf_468")
print(f"Channel name: {mysensor.get_channel_name(channel=channel_count)}")

# set the frequency
mysensor.set_channel_frequency(channel=channel_count, frq_mega_hz=468)
print(f"Channel frequency: {mysensor.get_channel_frequency(channel=channel_count)} MHz")

# set the bandwidth
mysensor.set_channel_bandwidth(channel=channel_count, bw=mysensor.bandwidth.bw12p5khz)
print(f"Channel bandwidth: {mysensor.get_channel_bandwidth(channel=channel_count)}")

# set the alarm state
mysensor.set_channel_alarm_enable(channel=channel_count, state=mysensor.ch_alarm_state.report)
print(f"Channel alarm state: {mysensor.get_channel_alarm_enable(channel=channel_count)}")

# set the min fwd power
mysensor.set_channel_power_min_limit(channel=channel_count, power=0.05)
print(f"Power min limit = {mysensor.get_channel_power_min_limit(channel=channel_count)} W")

# set the max fwd power
mysensor.set_channel_power_max_limit(channel=channel_count, power=12.54)
print(f"Power max limit: {mysensor.get_channel_power_max_limit(channel=channel_count)} W")

# set the min vswr
mysensor.set_channel_vswr_min_limit(channel=channel_count, vswr=1.01)
print(f"VSWR min limit: {mysensor.get_channel_vswr_min_limit(channel=channel_count)}")

# set the max vswr
mysensor.set_channel_vswr_max_limit(channel=channel_count, vswr=3.01)
print(f"VSWR max limit: {mysensor.get_channel_vswr_max_limit(channel=channel_count)}")

# set the max hold threshold state
mysensor.set_channel_max_hold_state(channel=channel_count, state=mysensor.max_hold_state.enable)
print(f"Max hold state: {mysensor.get_channel_max_hold_state(channel=channel_count)}")

# set the max hold forward power threshold
mysensor.set_channel_max_hold_threshold(channel=channel_count, power=23.5)
print(f"VSWR min limit: {mysensor.get_channel_max_hold_threshold(channel=channel_count)}")

# set the PTT response type
mysensor.set_channel_ptt_mode(channel=channel_count, mode=mysensor.ptt_mode.normally_open)
print(f"PTT mode: {mysensor.get_channel_ptt_mode(channel=channel_count)}")

# set the PTT input selection
mysensor.set_channel_ptt_input_index(channel=channel_count, input=2)
print(f"PTT input index: {mysensor.get_channel_ptt_input_index(channel=channel_count)}")

mysensor.remove_channel(channel=channel_count)
print("done")


