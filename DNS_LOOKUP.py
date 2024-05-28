import dns.resolver
import whois
import time
from datetime import datetime
from colorama import Fore, Style, init
import os
import io
import sys

init()  

def format_output(text, color=Fore.WHITE, delay=0.05):
    """Format the output with color, delay, and a hacker-like font"""
    font = "\033[1m"  
    for char in text:
        print(color + font + char, end="", flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def print_rainbow_text(text):
    """Print text with rainbow colors""" 
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        print(color + char, end='', flush=True)
    print(Style.RESET_ALL)

def print_palestine_flag_text(text):
    """Print text with Palestine flag colors"""
    flag_colors = [Fore.RED, Fore.WHITE, Fore.GREEN, Fore.RED]
    lines = text.split("\n")
    for line, color in zip(lines, flag_colors * (len(lines) // len(flag_colors) + 1)):
        print(color + line)
    print(Style.RESET_ALL)


print_rainbow_text(r"""
  ____     _   _    ____     _       U  ___ u   U  ___ u   _  __      _   _   ____       
 |  _"\   | \ |"|  / __"| u |"|       \/"_ \/    \/"_ \/  |"|/ /   U |"|u| |U|  _"\ u    
/| | | | <|  \| |><\___ \/U | | u     | | | |    | | | |  | ' /     \| |\| |\| |_) |/    
U| |_| |\U| |\  |u u___) | \| |/__.-,_| |_| |.-,_| |_| |U/| . \\u    | |_| | |  __/      
 |____/ u |_| \_|  |____/>> |_____|\_)-\___/  \_)-\___/   |_|\_\    <<\___/  |_|         
  |||_    ||   \\,-.)(  (__)//  \\      \\         \\   ,-,>> \\,-.(__) )(   ||>>_       
 (__)_)   (_")  (_/(__)    (_")("_)    (__)       (__)   \.)   (_/     (__) (__)__)
""")

def get_whois_info(domain):
    """Retrieve WHOIS information for the given domain"""
    try:
        whois_data = whois.whois(domain)
        return whois_data
    except Exception:
        return None

def search_other_domains(domain, whois_data):
    """Search for other domains owned by the same registrant"""
    try:
        if whois_data and "registrant" in whois_data and "name" in whois_data["registrant"]:
            registrant_name = whois_data["registrant"]["name"]
            format_output(f"Searching for other domains owned by {registrant_name}...", Fore.YELLOW)
            if "domain" in whois_data:
                any_other_domains = False
                for other_domain in whois_data["domain"]:
                    if other_domain != domain:
                        format_output(f"- {other_domain}", Fore.YELLOW)
                        any_other_domains = True
                if not any_other_domains:
                    format_output("No other domains found.", Fore.YELLOW)
            else:
                format_output("No other domains found.", Fore.YELLOW)
    except Exception:
        format_output("Error searching for other domains.", Fore.YELLOW)

class DualWriter:
    """A class to write output to both terminal and a StringIO buffer."""
    def __init__(self, original_stdout, buffer):
        self.original_stdout = original_stdout
        self.buffer = buffer

    def write(self, message):
        self.original_stdout.write(message)
        self.buffer.write(message)

    def flush(self):
        self.original_stdout.flush()
        self.buffer.flush()

def main():
    while True:
        website = input(Fore.RED + "Enter a website to look up (or 'q' to quit): " + Style.RESET_ALL)
        if website.lower() == "q":
            break

        
        output_buffer = io.StringIO()
        
        
        original_stdout = sys.stdout
        sys.stdout = DualWriter(original_stdout, output_buffer)

        format_output(f"Looking up {website}...", Fore.CYAN)

        record_types = ["A", "AAAA", "MX", "SOA", "CNAME"]
        for record_type in record_types:
            try:
                record = dns.resolver.resolve(website, record_type)
                if record:
                    if record_type == "A":
                        format_output(f"IPv4 record(s) for {website}:", Fore.GREEN)
                    elif record_type == "AAAA":
                        format_output(f"IPv6 record(s) for {website}:", Fore.GREEN)
                    elif record_type == "SOA":
                        format_output(f"SOA (Start of Authority) record for {website}:", Fore.GREEN)
                        for rdata in record:
                            format_output(f"- Primary Name Server: {rdata.mname}")
                            format_output(f"- Responsible Party's Email: {rdata.rname}")
                            format_output(f"- Serial Number: {rdata.serial}")
                            format_output(f"- Refresh Time: {rdata.refresh} seconds")
                            format_output(f"- Retry Time: {rdata.retry} seconds")
                            format_output(f"- Expire Time: {rdata.expire} seconds")
                            format_output(f"- Minimum TTL: {rdata.minimum} seconds")
                    elif record_type == "MX":
                        format_output(f"MX (Mail Exchange) record(s) for {website}:", Fore.GREEN)
                        for rdata in record:
                            format_output(f"- Priority: {rdata.preference}, Mail Server: {rdata.exchange}")
                    else:
                        format_output(f"{record_type} record(s) for {website}:", Fore.GREEN)
                    for rdata in record:
                        format_output(f"- {rdata}", Fore.GREEN)
            except (dns.resolver.NXDOMAIN, dns.resolver.Timeout, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
                pass

        whois_data = get_whois_info(website)
        if whois_data:
            format_output(f"WHOIS information for {website}:\n{whois_data}", Fore.YELLOW)
        else:
            format_output(f"WHOIS information not retrieved for {website}.", Fore.YELLOW)

        sys.stdout = original_stdout

        save_output = input(Fore.RED + "Do you want to save the output to a file? (y/n) " + Style.RESET_ALL)
        if save_output.lower() == "y":
            filename = input(Fore.RED + "Enter a filename or press Enter to use the default (DNS_LOOKUP.txt): " + Style.RESET_ALL)
            if not filename:
                filename = "DNS_LOOKUP.txt"
            with open(filename, "w") as file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"Output for {website} on {current_time}:\n\n")
                file.write(output_buffer.getvalue())
            format_output(f"Output saved to {filename}", Fore.CYAN)

        print()
        continue_search = input(Fore.RED + "Do you want to look up another website? (y/n) " + Style.RESET_ALL)
        if continue_search.lower() != "y":
            break

    
    print_palestine_flag_text(r"""
  _____ ____  _____ _____   ____   _    _     _____ ____ _____ ___ _   _ _____  
 |  ___|  _ \| ____| ____| |  _ \ / \  | |   | ____/ ___|_   _|_ _| \ | | ____| 
 | |_  | |_) |  _| |  _|   | |_) / _ \ | |   |  _| \___ \ | |  | ||  \| |  _|   
 |  _| |  _ <| |___| |___  |  __/ ___ \| |___| |___ ___) || |  | || |\  | |___  
 |_|   |_| \_\_____|_____| |_| /_/   \_\_____|_____|____/ |_| |___|_| \_|_____| 
""")

if __name__ == "__main__":
    main()
