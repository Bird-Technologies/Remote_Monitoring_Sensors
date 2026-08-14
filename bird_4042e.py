"""
@verbatim

The MIT License (MIT)

Copyright (c) 2026 Bird

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
import asyncio
from pysnmp.hlapi.asyncio import *

async def snmp_get(target_ip, community, oid):
        # Create the SNMP engine and dispatch the GET request
        error_indication, error_status, error_index, var_binds = await get_cmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),  # mpModel=1 is SNMPv2c
            await UdpTransportTarget.create((target_ip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        preamble = None
        payload = None

        # Error handling
        if error_indication:
            print(f"Engine Error: {error_indication}")
        elif error_status:
            print(f"SNMP Error: {error_status.prettyPrint()} at {error_index}")
        else:
            # Loop over bindings (usually 1 for a single GET request)
            for var_bind in var_binds:
                #print(f"{var_bind[0].prettyPrint()} = {var_bind[1].prettyPrint()}")
                preamble = var_bind[0].prettyPrint()
                payload = var_bind[1].prettyPrint()
        return preamble, payload

class Bird4042E_Sensor():
    """
    This is a driver. 
    """
    def __init__(self, ip_address):
        self.__ip_address = ip_address

    def model(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.2.0'
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload
    
    def system_description(self):
        oid = '1.3.6.1.2.1.1.1.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def system_uptime(self):
        oid = '1.3.6.1.2.1.1.3.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def name(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.1.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def serial_number(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.3.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def forward_power(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.14.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        fwd_pwr = float(payload)/10
        return fwd_pwr

    def reflected_power(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.15.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        rfl_pwr = float(payload)/10
        return rfl_pwr

    def vswr(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.16.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with two decimal points
        vswr = float(payload)/100
        return vswr

    def uptime(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.27.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        count = float(payload)
        days, remainder = divmod(int(payload), (3600 * 24))
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    def temperature(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.30.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        temper = float(payload)/10
        return temper
    
    def calibration_date(self):
        oid = '1.3.6.1.4.1.21581.1.7.300.31.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload
    
