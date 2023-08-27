import netmiko
import json
import re
from getpass import getpass
#======================================================================
# LESSON 1 - SSH Connection using netmiko 
# # print(dir(netmiko))
# devices='192.168.231.5'
# device_type='cisco_ios'
# username='cisco'
# password = 'cisco'

# connection = netmiko.ConnectHandler(ip=devices,device_type=device_type,username=username,password=password)
# # print(connection.send_command('show ip int brief'))  
# print(connection.send_command('show clock'))                                                                 
# connection.disconnect()

#=======================================================================
# LESSON 2 - Error Handling
# devices='''
# 192.168.231.11
# 192.168.231.12
# 192.168.231.13
# 192.168.231.14
# 192.168.231.15
# '''.strip().splitlines() # this will split the docstring and create an array of ip addresses

# device_type='cisco_ios'
# username='cisco'
# password = 'cisco'
# for device in devices:
#     try:
#         print(f'Connecting to device {device}')
#         connection = netmiko.ConnectHandler(ip=device,device_type=device_type,username=username,password=password)
#         # print(connection.send_command('show ip int brief'))
#         print(connection.send_command('show clock'))
#         print('============================================================')                                                                 
#         connection.disconnect()
#     except (netmiko.exceptions.NetmikoAuthenticationException,netmiko.exceptions.NetmikoTimeoutException) as error:
#         error_message = re.match(".*",str(error)).group(0)
#         print(f'Cannot connect to {device} due to {error_message}')
#         print('============================================================')  
#=======================================================================
# LESSON 3 - using Dictionary
# devices = [{'ip' :'192.168.231.11',
#             'device_type' : 'cisco_ios',
#             'username' : 'cisco',
#             'password' : 'cisco'
#             },
#             {'ip' :'192.168.231.12',
#             'device_type' : 'cisco_ios',
#             'username' : 'admin',
#             'password' : 'admin'
#             },
#             {'ip' :'192.168.231.13',
#             'device_type' : 'cisco_ios',
#             'username' : 'cisco',
#             'password' : 'cisco'
#             },
#             {'ip' :'192.168.231.14',
#             'device_type' : 'cisco_ios',
#             'username' : 'cisco',
#             'password' : 'cisco'
#             },
#             {'ip' :'192.168.231.15',
#             'device_type' : 'cisco_ios',
#             'username' : 'cisco',
#             'password' : 'cisco'
#             }]

# for device in devices:
#     try:
#         print(f'Connecting to device {device["ip"]}')
#         connection = netmiko.ConnectHandler(**device)
#         # print(connection.send_command('show ip int brief'))
#         print(connection.send_command('show clock'))
#         print('============================================================')                                                                 
#         connection.disconnect()
#     except (netmiko.exceptions.NetmikoAuthenticationException,netmiko.exceptions.NetmikoTimeoutException) as error:
#         error_message = re.match(".*",str(error)).group(0)
#         print(f'Cannot connect to {device["ip"]} due to {error_message}')
#         print('============================================================')  
#=======================================================================
# LESSON 4 - JSON and Getpass

# username = input('Enter username: ')
# password = getpass.getpass(prompt='Enter password: ') # getpass function will not echo the input given, so password will be hidden
# with open ('devices.json') as dev_file:
#     devices = json.load (dev_file) # import the values from json file into the variable

# for device in devices:
#     device['username'] = username
#     device['password'] = password
#     try:
#         print(f'Connecting to device {device["ip"]}')
#         connection = netmiko.ConnectHandler(**device)
#         # print(connection.send_command('show ip int brief'))
#         print(connection.send_command('show clock'))
#         print('============================================================')                                                                 
#         connection.disconnect()
#     except (netmiko.exceptions.NetmikoAuthenticationException,netmiko.exceptions.NetmikoTimeoutException) as error:
#         error_message = re.match(".*",str(error)).group(0)
#         print(f'Cannot connect to {device["ip"]} due to {error_message}')
#         print('============================================================') 
#=======================================================================
# LESSON 5 - completing script

# def get_credentials():
#     '''
#     Created a function to get credentials 
#     as well as verify the password by matching it twice
#     '''
#     username = input("Enter username: ")
#     password = None
#     while not password:
#         password = getpass("Enter your password")
#         password_verify = getpass('Retype your password: ')
#         if password!=password_verify:
#             print('Password do not match, try again')
#             password = None
#     return username,password     
 
# username,password = get_credentials()
# with open ('devices.json') as dev_file:
#     devices = json.load (dev_file) # import the values from json file into the variable

# for device in devices:
#     device['username'] = username #values are added to dictionary before sending it to netmiko
#     device['password'] = password
#     try:
        
#         print(f'Connecting to device {device["ip"]}')
#         connection = netmiko.ConnectHandler(**device)
#         # print(connection.send_command('show ip int brief'))
#         with open('switch_commands.txt','r') as commands:
#             for command in commands:
#                 print('## Output of '+command+'\n')
#                 print(connection.send_command(command))
#         # print('============================================================')                                                                 
#         connection.disconnect()
#     except (netmiko.exceptions.NetmikoAuthenticationException,netmiko.exceptions.NetmikoTimeoutException) as error:
#         error_message = re.match(".*",str(error)).group(0)
#         print(f'Cannot connect to {device["ip"]} due to {error_message}')
#         print('============================================================') 

#=======================================================================
# testing script


known_neighbors = {}
known_ip = [] 
username,password = 'cisco','cisco'
with open ('devices.json') as dev_file:
    devices = json.load (dev_file) # import the values from json file into the variable

for device in devices:
    device['username'] = username #values are added to dictionary before sending it to netmiko
    device['password'] = password
    try:
        
        print(f'Connecting to device {device["ip"]}')
        connection = netmiko.ConnectHandler(**device)
        node_name = connection.send_command('sh run | include host')
        cdp_output = connection.send_command('show cdp neighbors detail')
        # print(str(cdp_output))
        neighbors = re.findall("Device ID: .+\n.*:.*\n.*:.*\n",str(cdp_output))
        for neighbor in neighbors:
            op_nbr = re.match("Device ID: (.*)\..*\..*\n.*\n.*: (.*)",str(neighbor))
            known_neighbors[op_nbr.group(1)] = op_nbr.group(2)
            if op_nbr.group(2) not in known_ip:
                known_ip.append(op_nbr.group(2))   # add it to queue after verifiying it is unique
                print(f"{node_name[9:]},{op_nbr.group(1)}")
                # edge_list.append((node_name[9:],op_nbr.group(1),{"type":"copper"})) 
        connection.disconnect()
        print(known_neighbors)
        print(known_ip)
        print(node_name[9:])
    except (netmiko.exceptions.NetmikoAuthenticationException,netmiko.exceptions.NetmikoTimeoutException) as error:
        error_message = re.match(".*",str(error)).group(0)
        print(f'Cannot connect to {device["ip"]} due to {error_message}')
        print('============================================================') 