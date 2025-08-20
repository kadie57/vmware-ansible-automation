#!/usr/bin/env python3

import asyncio
import aiohttp
import json
import ssl
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def main(queue, args):
    """The entry point plugin uses the vCenter API"""
    
    host = args['host']
    username = args['username']
    password = args['password']
    
    print(f" Monitoring vCenter {host} qua API...")
    

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        login_url = f"https://{host}/rest/com/vmware/cis/session"
        auth = aiohttp.BasicAuth(username, password)
        
        async with session.post(login_url, auth=auth) as response:
            if response.status != 200:
                print(f" Login error: {response.status}")
                return
                
            session_data = await response.json()
            session_id = session_data['value']
            
        print(" Login successful! Waiting for new VM...")
        
        session.headers['vmware-api-session-id'] = session_id
        
        vm_url = f"https://{host}/rest/vcenter/vm"
        async with session.get(vm_url) as response:
            initial_vms = await response.json()
            vm_names = {vm['vm'] for vm in initial_vms['value']}
            
        print(f"Monitoring {len(vm_names)} VMs currently...")
        
        # Monitor loop
        while True:
            try:
                async with session.get(vm_url) as response:
                    if response.status == 200:
                        current_vms = await response.json()
                        current_vm_names = {vm['vm'] for vm in current_vms['value']}
                        
                        new_vms = current_vm_names - vm_names
                        
                        for vm_id in new_vms:
                            vm_detail_url = f"https://{host}/rest/vcenter/vm/{vm_id}"
                            async with session.get(vm_detail_url) as detail_response:
                                if detail_response.status == 200:
                                    vm_detail = await detail_response.json()
                                    vm_name = vm_detail['value']['name']

                                    event = {
                                        'vm_name': vm_name,
                                        'vm_id': vm_id,
                                        'vcenter_host': host,
                                        'timestamp': datetime.now().isoformat()
                                    }
                                    await queue.put(event)
 
                        vm_names = current_vm_names
                        
                await asyncio.sleep(15)  
                
            except Exception as e:
                print(f"❌ Lỗi: {e}")
                await asyncio.sleep(15)
