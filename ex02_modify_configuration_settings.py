"""
Example Description:
    This example shows how to modify the 4042E remote power monitor/sensor
    configuration settings. 
    
    NOTE: This requires the 'SNMP Sets' value to be enabled.

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

mysensor = Bird4042E_Sensor("192.168.3.200")

print(f"Model: {mysensor.get_model()}")
print(f"Name: {mysensor.get_name()}")

print(f"Settings before modification...\n==========")
print(f"Max Aggregate Power Limit = {mysensor.get_power_max_limit()} W")
print(f"Min Aggregate Power Limit = {mysensor.get_power_min_limit()} W")
print(f"VSWR Min Limit = {mysensor.get_min_vswr_limit()}")
print(f"VSWR Max Limt = {mysensor.get_max_vswr_limit()}")

mysensor.set_power_max_limit(100.0)
mysensor.set_power_min_limit(0.0)
mysensor.set_vswr_min_limit(1.0)
mysensor.set_vswr_max_limit(2.0)

print(f"Settings after modification...\n==========")
print(f"Max Aggregate Power Limit = {mysensor.get_power_max_limit()} W")
print(f"Min Aggregate Power Limit = {mysensor.get_power_min_limit()} W")
print(f"VSWR Min Limt = {mysensor.get_min_vswr_limit()}")
print(f"VSWR Max Limt = {mysensor.get_max_vswr_limit()}")



