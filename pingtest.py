import os
import requests
import logging
import argparse
from datetime import datetime
from time import sleep 

def setup_log():
    # Make a ./log directory in the current working directory if it doesn't exist yet.
    cwd = os.getcwd()

    try: 
        os.mkdir(os.path.join(cwd, 'log'))
    except FileExistsError as e: 
        # don't worry if the directory already exists
        # but if there's some other error it will fail
        pass 

    date = datetime.today().strftime('%Y-%m-%d')
    logging.basicConfig(filename='log/pingtest-' + date + '.log', level=logging.WARNING)

def main():
    urls = [ # added IP addresses to see if DNS-only issue
            {'hostname':'http://imgur.com','ip':'http://151.101.56.193' },
            {'hostname':'http://python.org', 'ip':'http://45.55.99.72' },
            {'hostname':'http://yahoo.com', 'ip':'http://72.30.35.9' },
            {'hostname':'http://google.com', 'ip':'http://64.233.177.102'} ,
            {'hostname':'http://reddit.com', 'ip':'http://151.101.65.140' },
            {'hostname':'http://netgear.com', 'ip':'http://13.248.140.194' },
        ]

    s = requests.Session()

    parser = argparse.ArgumentParser(description='Ping a set of hosts and log if one cannot be reached.')
    parser.add_argument('--sleep', type=int, help='number of seconds to sleep between pings')
    args = parser.parse_args()

    if args.sleep: 
        SLEEP = args.sleep 
    else:
        SLEEP = 15 

    while True: 
        for target in urls: 
            # first try to connect to hostname like google.com
            try: 
                timestamp = datetime.now()

                r = s.get(url=target['hostname'], stream=False)
                logging.info(' {} : connected to {} successfully'.format(timestamp, target['hostname']))

            except Exception as e:
                logging.error(' {} : could not connect to {} trying IP address'.format(timestamp, target['hostname']))
                logging.error(' {} : Error message : {}'.format(timestamp, e))

                # next, try the IP directly
                try: 
                    r = s.get(url=target['ip'], stream=False)
                    logging.warning(' {} : Connected to {} successfully but {} failed'.format(timestamp, target['ip'], target['hostname']))
                except Exception as e: 
                    logging.error(' {} : Error - could not connect to hostname or IP: {}'.format(timestamp, e))

            sleep(SLEEP) 

if __name__ == '__main__':
    setup_log()
    main()







