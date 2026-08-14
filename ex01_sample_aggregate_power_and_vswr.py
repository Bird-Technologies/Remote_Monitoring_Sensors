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

mysensor = Bird4042E_Sensor("192.168.3.200")

print(f"Model: {mysensor.model()}")
print(f"Name: {mysensor.name()}")
print(f"Description: {mysensor.system_description()}")
print(f"Serial Num.: {mysensor.serial_number()}")
print(f"Cal Date: {mysensor.calibration_date()}")
print(f"Uptime: {mysensor.uptime()}")
print(f"Temperature: {mysensor.temperature()}\u00b0C")

for j in range(30):
    print(f"forward = {mysensor.forward_power()}, reflected = {mysensor.reflected_power()}, vswr = {mysensor.vswr()}")