from typing import List
import re
import json



def ping_latencies(ping_output: bytes) -> List:

    ping_latencies = {nr: -1 for nr in range(1, 6)}
#    for line in ping_output.encode().decode('utf-8').split('\n'):
    for line in ping_output.encode().decode('utf-8').split('\n'):
        nr_match = re.search("icmp_seq=(\d+) ", line)
        if nr_match:
            nr = int(nr_match.group(1))
        else:
            continue

        time_match = re.search("time=(\d+(\.(\d+))?) ms", line)
        if time_match:
            ping_latencies[nr] = float(time_match.group(1))
        else:
            if 'filtered' in line:
                ping_latencies[nr] = -2

    # Some ping implementations start counting at 0
    # If so, nr goes from 0-4 instead of 1-5
    if 0 in ping_latencies:
        del ping_latencies[5]

    return [ping_latencies[key] for key in sorted(ping_latencies.keys())]
    
    
def ping_ttls(ping_output: bytes) -> List:

    ping_ttls = {nr: -1 for nr in range(1, 6)}
#    for line in ping_output.encode().decode('utf-8').split('\n'):
    for line in ping_output.encode().decode('utf-8').split('\n'):
        nr_match = re.search("icmp_seq=(\d+) ", line)
        if nr_match:
            nr = int(nr_match.group(1))
        else:
            continue

        time_match = re.search("ttl=(\d+) ", line)
        if time_match:
            ping_ttls[nr] = int(time_match.group(1))
        else:
            if 'filtered' in line:
                ping_ttls[nr] = -2

    # Some ping implementations start counting at 0
    # If so, nr goes from 0-4 instead of 1-5
    if 0 in ping_ttls:
        del ping_ttls[5]

    return [ping_ttls[key] for key in sorted(ping_ttls.keys())]
    
def parse_ping(ping_output: bytes):

   # print(ping_latencies(ping_output))
   # print(ping_ttls(ping_output))
   latencies = ping_latencies(ping_output)
   ttls = ping_ttls(ping_output)
   tablen = len(latencies)

   json_data = {}
   json_results = []
   
   for i in range(tablen):
	   
	   results = {}
	 #  print(latencies[i] )
	   
	   if latencies[i] == -2:
		   results['status'] = 'filtered'
		   results['ttl'] = 'Null'
		   results['latency'] = 'Null'
		   json_results.append(results)
	   
	   elif latencies[i] != -2 :
		   results['status'] = 'ok'
		   results['ttl'] = ttls[i]
		   results['latency'] = latencies[i]
		   json_results.append(results)
		   
   json_data['reults'] = json_results
   json_data['address'] = 'wert'
   json_data['success'] = True
   json_data['reason'] = "All ok"
   
   
   return(json_data)

def punyHostname(hostname):
#       str = hostname.encode().decode('utf-8')
#       out = str.encode('punycode')
#       return out.decode()
#       url_parts = urlparse(hostname, scheme='http')
#       return url_parts.netloc.encode('idna').decode('utf-8')
        return hostname
	
def marvinPingParser(hostname, data, ping_output):
	result = {}
	data["destination"] = punyHostname(hostname)
	result["results"] = parse_ping(ping_output)
	result["request"] = data.copy()	
	
	return(result)
    
def main():
	output = """PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=57 time=25.1 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=57 time=15.1 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=57 time=22.0 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=60 time=22.0 ms
64 bytes from 8.8.8.8: icmp_seq=5 ttl=59 time=22.0 ms
64 bytes from 8.8.8.8: icmp_seq=6 ttl=59 time=22.0 ms
From 172.17.5.253 icmp_seq=7 Packet filtered
From 172.17.5.253 icmp_seq=8 Packet filtered

--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2001ms
rtt min/avg/max/mdev = 15.130/20.767/25.124/4.182 ms"""
	
	print(output)
	
	result = marvinPingParser('8.8.8.8', {'count': 3, 'size': 56, 'pmtu': 'want', 'timeout': 60}, output)
	
	#parse_ping(output)
	
	print(json.dumps(result, indent=4))


if __name__  == "__main__":
	main()