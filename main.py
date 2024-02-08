from fastapi import FastAPI, HTTPException, Query, status, Response
from intervaltree import IntervalTree, Interval
import ipaddress
app = FastAPI()

def load_ip_range(file):
    
    ranges = []
    file = open('IN-suip.biz.txt','r')
    for line in file:
        start, end = line.strip().split('-')
        ranges.append(Interval(ipaddress.IPv4Address(start), ipaddress.IPv4Address(end)))
        return ranges

def load_ip_range(file1):
    
    ranges = []
    file1 = open('CN-suip.biz.txt','r')
    for line in file1:
            start, end = line.strip().split('-')
            ranges.append(Interval(ipaddress.IPv4Address(start), ipaddress.IPv4Address(end)))
    return ranges

def load_ip_range(file2):
    
    ranges = []
    file2 = open('PK-suip.biz.txt','r')
    for line in file2:
            start, end = line.strip().split('-')
            ranges.append(Interval(ipaddress.IPv4Address(start), ipaddress.IPv4Address(end)))
    return ranges

def construct_interval_tree(ranges):
    
    tree = IntervalTree()
    for interval in ranges:
        tree.add(interval)
    return tree

countries = {
    'India': 'IN-suip.biz.txt',
    'China': 'CN-suip.biz.txt',
    'Pakistan': 'PK-suip.biz.txt'
}

country_interval_trees = {}

for country, file in countries.items():
    ranges = load_ip_range(file)
    interval_tree = construct_interval_tree(ranges)
    country_interval_trees[country] = interval_tree

country_interval_trees = {}

for country, file1 in countries.items():
    ranges = load_ip_range(file1)
    interval_tree = construct_interval_tree(ranges)
    country_interval_trees[country] = interval_tree

country_interval_trees = {}

for country, file2 in countries.items():
    ranges = load_ip_range(file2)
    interval_tree = construct_interval_tree(ranges)
    country_interval_trees[country] = interval_tree



@app.get("/check-ip")
async def check_ip(country: str = Query(..., description="Country name"), ip_address: str = Query(..., description="IP Address")):
    if country.lower() not in countries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country with this ip {ip_address} is not available")

    if not any(country_tree[ip_address] for country_tree in country_interval_trees.values()):
        return {"belongs_to_country": False}

    country_tree = country_interval_trees[country.lower()]
    if any(country_tree[ip_address]):
        return {"belongs_to_country": True, "country": country}

    return {"belongs_to_country": False}



