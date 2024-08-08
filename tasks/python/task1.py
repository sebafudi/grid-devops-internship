import os

def get_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    if not file_extension:
        raise ValueError("File has no extension")
    return file_extension

# Example usage:
print(get_file_extension("example.txt"))  # Output: .txt
# Task 2: Remove duplicates and find min/max

def remove_duplicates_and_find_min_max(numbers):
    unique_numbers = tuple(set(numbers))
    return min(unique_numbers), max(unique_numbers)

# Example usage:
numbers = [1, 2, 2, 3, 4, 4, 5]
min_num, max_num = remove_duplicates_and_find_min_max(numbers)
print(min_num, max_num)  # Output: 1 5
# Task 3: Parse access log

import re
from collections import defaultdict

# def parse_access_log(file_name):
#     user_agents = defaultdict(int)
#     with open(file_name, 'r') as file:
#         for line in file:
#             match = re.search(r'"(.+?)"', line)
#             if match:
#                 user_agent = match.group(1)
#                 user_agents[user_agent] += 1
#     total_user_agents = len(user_agents)
#     return total_user_agents, dict(user_agents)

# # Example usage:
# total_user_agents, user_agent_stats = parse_access_log("access.log")
# print(total_user_agents)
# print(user_agent_stats)
# # Task 4: Count character occurrences

import re
from collections import defaultdict

def parse_access_log(file_name):
    """
    Reads an access log file and returns the total number of different User Agents
    and a dictionary with the number of requests from each User Agent.

    Args:
        file_name (str): The name of the access log file.

    Returns:
        int: The total number of different User Agents.
        dict: A dictionary with the number of requests from each User Agent.
    """
    user_agents = defaultdict(int)
    with open(file_name, 'r') as file:
        for line in file:
            match = re.search(r'"[^"]+" "([^"]+)"', line)
            if match:
                user_agent = match.group(1)
                user_agents[user_agent] += 1
    total_user_agents = len(user_agents)
    return total_user_agents, dict(user_agents)

def main():
    file_name = "access.log"
    total_user_agents, user_agent_stats = parse_access_log(file_name)
    print(f"Total number of different User Agents: {total_user_agents}")
    print("Number of requests from each User Agent (sorted by occurrences):")
    for user_agent, count in sorted(user_agent_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"{user_agent}: {count}")

if __name__ == "__main__":
    main()

def count_character_occurrences(input_string):
    character_occurrences = {}
    for char in input_string:
        if char in character_occurrences:
            character_occurrences[char] += 1
        else:
            character_occurrences[char] = 1
    return character_occurrences

# # Example usage:
input_string = "pythonnohtyppy"
character_occurrences = count_character_occurrences(input_string)
for char, count in character_occurrences.items():
    print(f"{char}: {count}")
# Task 5: Get system information

import platform
import psutil
import argparse

def get_system_info(args):
    system_info = {}
    if args.distro:
        system_info["distro"] = platform.platform()
    if args.memory:
        memory = psutil.virtual_memory()
        system_info["memory_total"] = memory.total
        system_info["memory_used"] = memory.used
        system_info["memory_free"] = memory.free
    if args.cpu:
        cpu = psutil.cpu_times()
        system_info["cpu_model"] = platform.processor()
        system_info["cpu_core_numbers"] = psutil.cpu_count()
        system_info["cpu_speed"] = psutil.cpu_freq().current
    if args.user:
        system_info["current_user"] = platform.node()
    if args.load_average:
        system_info["load_average"] = psutil.getloadavg()
    if args.ip_address:
        system_info["ip_addresses"] = {}
        for interface, addresses in psutil.net_if_addrs().items():
            if addresses and addresses[0]:
                system_info["ip_addresses"][interface] = addresses[0].address
    return system_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--distro", action="store_true")
    parser.add_argument("-m", "--memory", action="store_true")
    parser.add_argument("-c", "--cpu", action="store_true")
    parser.add_argument("-u", "--user", action="store_true")
    parser.add_argument("-l", "--load_average", action="store_true")
    parser.add_argument("-i", "--ip_address", action="store_true")
    args = parser.parse_args()
    system_info = get_system_info(args)
    for key, value in system_info.items():
        if key == "ip_addresses":
            print(f"{key}:")
            for interface, ip_address in value.items():
                print(f"  {interface}: {ip_address}")
        else:
            print(f"{key}: {value}")