import json
from DataFetcher import *
from rich.console import Console
from rich.text import Text
from time import sleep

# Initialize console
console = Console()

# Load configuration
def load_config():
    with open('E:\Coding\SpecSnap\config.json', 'r') as f:
        return json.load(f)

config = load_config()

# Gradient text function
def gradient_text(text, colors):
    steps = len(text)
    gradient = Text()
    color_steps = len(colors) - 1

    for i, char in enumerate(text):
        if char.strip():
            color_index = int(i / steps * color_steps)
            start_color = colors[color_index]
            end_color = colors[color_index + 1]
            
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i % (steps // color_steps)) / (steps // color_steps))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i % (steps // color_steps)) / (steps // color_steps))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i % (steps // color_steps)) / (steps // color_steps))
            
            gradient.append(char, style=f"rgb({r},{g},{b})")
        else:
            gradient.append(char)
    
    return gradient

# Helper function to print data with optional gradient
def print_with_style(text):
    if config["output"]["enable_colors"] and config["output"]["gradient"]["enabled"]:
        colors = config["output"]["gradient"]["colors"]
        console.print(gradient_text(text, colors))
    else:
        console.print(text)

# Main testing function
def test_data_fetch():
    test_results = {}
    
    # Map functions to config keys
    tests = {
        "Operating_System": get_os_info,
        "CPU_Information": get_cpu_info,
        "GPU_Information": get_gpu_info,
        "Memory_Information": get_memory_info,
        "Storage_Information": get_storage_info,
        "Network_Information": lambda: {
            "IP Address": get_ip_info(),
            "Wi-Fi SSID": get_wifi_ssid(),
            "MAC Address": get_mac_address(),
            "Hostname": get_hostname()
        },
        "Shell_Information": lambda: {
            "Shell": get_shell_info(),
            "Uptime": get_uptime()
        },
        "User_Information": lambda: {
            "Username": get_user_info(),
            "Host": get_hostname()
        },
        "Process_Information": lambda: {
            "Process Count": get_process_count(),
            "High Usage Processes": get_high_usage_processes()
        },
        "Battery_Information": get_battery_info,
        "Performance_Information": lambda: {
            "CPU Usage": get_cpu_usage(),
            "Memory Usage": get_memory_usage()
        },
        "Display_Information": get_display_info
    }

    # Loop through categories based on config
    for category, details in config["data_categories"].items():
        if details["enabled"]:
            try:
                # Run the function associated with the category
                result = tests[category]()
                if isinstance(result, dict):
                    # Display specific fields if result is a dictionary and fields are specified
                    fields = details.get("fields", [])
                    output = f"[bold underline]{category}:[/bold underline]\n"
                    for field in fields:
                        if field in result:
                            output += f"{field}: {result[field]}\n"
                else:
                    # If result is not a dictionary, display it directly
                    output = f"[bold underline]{category}:[/bold underline] {result}\n"
                test_results[category] = output
            except Exception as e:
                test_results[category] = f"[bold red]{category} FAIL: {e}[/bold red]\n"

    # Print title if specified
    title = config["output"].get("display_title", "System Snapshot")
    print_with_style(f"[bold underline]{title}[/bold underline]")

    # Print each result
    for result in test_results.values():
        print_with_style(result)

# Run the test at specified refresh rate
refresh_rate = config.get("refresh_rate", 5)
while True:
    console.clear()
    test_data_fetch()
    sleep(refresh_rate)
