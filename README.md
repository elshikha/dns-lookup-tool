# dns-lookup-tool

## Introduction
This is a Python script for performing DNS lookups and retrieving WHOIS information for a given domain. It provides a command-line interface for users to input a domain name and get various DNS records along with WHOIS data.

## Features
- Look up DNS records such as A, AAAA, MX, SOA, and CNAME.
- Retrieve WHOIS information for a domain.
- Search for other domains owned by the same registrant.
- Save the output to a text file.

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/dns-lookup-tool.git
2. Navigate to the project directory:
   ```bash
   cd dns-lookup-tool
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
## Usage
- Make An Alias
   ```bash
   alias dns-lookup='python /dns-lookup-tool/DNS_LOOKUP.py'
- Now:
   ```bash
   dns-lookup
![dns-lookup-tool runtime](runtime.jpg)
