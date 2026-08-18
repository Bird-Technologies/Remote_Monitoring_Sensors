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
from enum import Enum

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

async def snmp_set(target_ip, community, oid, data_type, value):
    """
    Performs an SNMP SET request.
    data_type can be: Integer, OctetString, etc.
    """
    
    # Map raw value to appropriate PySNMP type
    if data_type == 'int':
        typed_value = Integer(int(value))
    elif data_type == 'str':
        typed_value = OctetString(str(value))
    else:
        raise ValueError("Unsupported data type mapping in this helper function.")

    # Execute the SET command
    errorIndication, errorStatus, errorIndex, varBinds = await set_cmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1), # mpModel=1 corresponds to SNMPv2c
        await UdpTransportTarget.create((target_ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), typed_value)
    )
    preamble = None
    payload = None

    # Evaluate response
    #errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Network Error: {errorIndication}")
    elif errorStatus:
        print(f"SNMP Error: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for varBind in varBinds:
            preamble = varBind[0].prettyPrint()
            payload = varBind[1].prettyPrint()
            #print(' = '.join([x.prettyPrint() for x in varBind]))
    return preamble, payload

class Bird4042E_Sensor():
    """
    This is a driver. 
    """
    def __init__(self, ip_address):
        self.__ip_address = ip_address

    def get_model(self)->str:
        oid = '1.3.6.1.4.1.21581.1.7.300.2.0'
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload
    
    def get_system_description(self)->str:
        oid = '1.3.6.1.2.1.1.1.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def get_system_uptime(self):
        oid = '1.3.6.1.2.1.1.3.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def get_name(self)->str:
        oid = '1.3.6.1.4.1.21581.1.7.300.1.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def get_serial_number(self)->str:
        oid = '1.3.6.1.4.1.21581.1.7.300.3.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload

    def get_forward_power(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.14.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        fwd_pwr = float(payload)/10
        return fwd_pwr

    def get_reflected_power(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.15.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        rfl_pwr = float(payload)/10
        return rfl_pwr

    def get_vswr(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.16.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with two decimal points
        vswr = float(payload)/100
        return vswr

    def get_uptime(self)->str:
        oid = '1.3.6.1.4.1.21581.1.7.300.27.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        count = float(payload)
        days, remainder = divmod(int(payload), (3600 * 24))
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days}:{hours:02}:{minutes:02}:{seconds:02}"

    def get_temperature(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.30.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        temper = float(payload)/10
        return temper
    
    def get_calibration_date(self)->str:
        oid = '1.3.6.1.4.1.21581.1.7.300.31.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        return payload
    
    def get_vswr_min_limit(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.4.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        temper = float(payload)/100
        return temper 
    
    def get_vswr_max_limit(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.6.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        temper = float(payload)/100
        return temper 
    
    def set_vswr_min_limit(self, max):
        oid_val = '1.3.6.1.4.1.21581.1.7.300.4.0'
        new_value = int(max*100)
        asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_val, data_type='int', value=new_value))
    
    def set_vswr_max_limit(self, max):
        oid_val = '1.3.6.1.4.1.21581.1.7.300.6.0'
        new_value = int(max*100)
        asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_val, data_type='int', value=new_value))
    
    def get_power_min_limit(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.8.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        temper = float(payload)/10
        return temper 
    
    def get_power_max_limit(self)->float:
        oid = '1.3.6.1.4.1.21581.1.7.300.10.0'
        # Example usage: Get system description (sysDescr)
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid))
        # The returned value will need to be a numeric with a single decimal point
        temper = float(payload)/10
        return temper 
    
    def set_power_min_limit(self, max):
        oid_val = '1.3.6.1.4.1.21581.1.7.300.8.0'
        new_value = int(max*10)
        asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_val, data_type='int', value=new_value))
    
    def set_power_max_limit(self, max):
        oid_val = '1.3.6.1.4.1.21581.1.7.300.10.0'
        new_value = int(max*10)
        asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_val, data_type='int', value=new_value))
    
    def get_channel_name(self, channel:int=1)->str:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.2.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return payload
    
    def set_channel_name(self, channel:int=1, name:str="ch_01"):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.2.{channel}')

        asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='str', value=name))
    
    def get_channel_frequency(self, channel:int=1)->float:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.14.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return float(payload)/1000000
    
    def set_channel_frequency(self, channel:int=1, frq_mega_hz:int=300):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.14.{channel}')

        # add checker code to ensure the channel range is 100 to 1000 MHz
        frq = frq_mega_hz * 1000000
        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=frq))
        return preamble, float(payload)/1000000
    
    class bandwidth(Enum):
        bw25khz = 1
        bw12p5khz = 2
        bw6p25khz = 3

    def get_channel_bandwidth(self, channel:int=1)->int:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.15.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return payload
    
    def set_channel_bandwidth(self, channel:int=1, bw:bandwidth=bandwidth.bw25khz):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.15.{channel}')

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=bw.value))
        return preamble, int(payload)
    
    class ch_alarm_state(Enum):
        disable = 1
        report = 2
        hca_1 = 3
        hca_2 = 4
        all = 5

    def get_channel_alarm_enable(self, channel:int=1)->int:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.27.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return int(payload)
    
    def set_channel_alarm_enable(self, channel:int=1, state:ch_alarm_state=ch_alarm_state.disable):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.27.{channel}')

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=state.value))
        return preamble, int(payload)
    
    def get_channel_power_min_limit(self, channel:int=1)->float:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.10.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return float(payload)/10
    
    def set_channel_power_min_limit(self, channel:int=1, power:float=0):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.10.{channel}')
        power = int(power*10)

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=power))
        return preamble, int(payload)
    
    def get_channel_power_max_limit(self, channel:int=1)->float:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.12.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return float(payload)/10
    
    def set_channel_power_max_limit(self, channel:int=1, power:float=0):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.12.{channel}')
        power = int(power*10)

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=power))
        return preamble, int(payload)
    
    def get_channel_vswr_min_limit(self, channel:int=1)->float:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.6.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return float(payload)/100
    
    def set_channel_vswr_min_limit(self, channel:int=1, vswr:float=0):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.6.{channel}')
        vswr = int(vswr*100)

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=vswr))
        return preamble, int(payload)
    
    def get_channel_vswr_max_limit(self, channel:int=1)->float:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.8.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return float(payload)/100
    
    def set_channel_vswr_max_limit(self, channel:int=1, vswr:float=0):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.8.{channel}')
        vswr = int(vswr*100)

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=vswr))
        return preamble, int(payload)
    
    class max_hold_state(Enum):
        disable = 1
        enable = 2

    def get_channel_max_hold_state(self, channel:int=1)->int:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.4.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return int(payload)
    
    def set_channel_max_hold_state(self, channel:int=1, state:max_hold_state=max_hold_state.disable):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.4.{channel}')

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=state.value))
        return preamble, int(payload)
    
    def get_channel_max_hold_threshold(self, channel:int=1)->float:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.5.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return float(payload)/10
    
    def set_channel_max_hold_threshold(self, channel:int=1, power:float=500):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.5.{channel}')
        power = int(power*10)

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=power))
        return preamble, int(payload)
    
    class ptt_mode(Enum):
        disable = 1
        normally_open = 2
        normally_closed = 3

    def get_channel_ptt_mode(self, channel:int=1)->int:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.16.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return int(payload)
    
    def set_channel_ptt_mode(self, channel:int=1, mode:ptt_mode=ptt_mode.disable):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.16.{channel}')

        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=mode.value))
        return preamble, int(payload)
    
    def get_channel_ptt_input_index(self, channel:int=1)->int:
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.17.{channel}')
        
        preamble, payload = asyncio.run(snmp_get(self.__ip_address, 'public', oid_base))
        return int(payload)
    
    def set_channel_ptt_input_index(self, channel:int=1, input:int=1):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.17.{channel}')
        
        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=input))
        return preamble, int(payload)
    
    def get_channel_count(self)->int:
        # do it the dumb way until a better method can be determined
        count = 0
        for j in range(1, 16+1):
            answer = self.get_channel_name(channel=j)
            if "No Such Instance" in answer:
                break
            else:
                count += 1
        
        return count
    
    def add_channel(self):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.321.0')
        preamble = None
        payload = None
        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=1))
        return preamble, int(payload)
    
    def remove_channel(self, channel:int=16):
        # add checker code to ensure the channel range is from 1 to 16...
        oid_base = format(f'1.3.6.1.4.1.21581.1.7.320.1.26.{channel}')
        preamble = None
        payload = None
        preamble, payload = asyncio.run(snmp_set(target_ip=self.__ip_address, community='public', oid=oid_base, data_type='int', value=1))
        return preamble, int(payload)
