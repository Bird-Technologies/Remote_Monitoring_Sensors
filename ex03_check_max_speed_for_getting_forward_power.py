"""
Example Description:
    This example is used to get a feel for how quickly the code will allow the
    4042E to respond to GETs of forward power.

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

rdgs_count = 100
t1 = time.time()
for j in range(rdgs_count):
    print(f"forward = {mysensor.get_forward_power()} W")
t2 = time.time()

rdg_per_sec = rdgs_count/(t2-t1)

print(f"{rdg_per_sec} rdg/sec")
