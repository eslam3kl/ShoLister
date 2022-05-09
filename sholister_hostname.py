from shodan import Shodan
from shodan.cli.helpers import get_api_key
from termcolor import colored
import sys

header1 = r'''
  _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( s | h | o | l | i | s | t | e | r )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ v0.1

Hostname search using [hostname] and [Ssl.cert.subject.CN] Filters.
Coded By: Eslam Akl (@eslam3kll)
'''
print(colored(header1, 'white', attrs=['bold']))
main_domains_file = sys.argv[1]
api = Shodan(get_api_key())
limit = 1000
counter = 0
results = []
with open(main_domains_file, 'r') as domains:
    try:
        for line in domains:
            line = line.strip()
            filename = line + '_shodan.txt'
            f = open(filename, 'a+')
            print(colored("[+] Searching for: ", 'green') + line)
            
            # ssl search 
            ssl_query = 'Ssl.cert.subject.CN:"' + line + '" 200'
            for banner in api.search_cursor(ssl_query):
                for hostname in banner['hostnames']:
                    #print(hostname)
                    if line in hostname:
                        results.append(hostname)
                counter += 1
                if counter >= limit:
                    break
            # hostname search 
            hostname_query = 'hostname:"' + line + '" 200'
            for banner in api.search_cursor(hostname_query):
                for hostname in banner['hostnames']:
                    #print(hostname)
                    if line in hostname:
                        if hostname not in results:
                            results.append(hostname)
                counter += 1
                if counter >= limit:
                    break
            results_length = len(results)
            print(colored("-> Found " + str(results_length) + " unique result for subdomain ["+ line + "] responds with status code [200 OK]", 'cyan'))
            print(colored("-> Output file name: " + filename, 'cyan') + "\n")
            # get results to output file
            for line in results:
                f.write(line + "\n")
            f.close()
            results = []

    except KeyboardInterrupt:
        print(colored("\nKeyboardInterrupt detected! GoodBye", 'red'))
        pass


