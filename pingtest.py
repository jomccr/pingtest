import os
import requests
import logging
from datetime import datetime
from time import sleep 

def main():
    urls = [ # added IP addresses to see if DNS-only issue
            {'hostname':'http://google.com', 'ip':'http://64.233.177.102'} ,
            {'hostname':'http://reddit.com', 'ip':'http://151.101.65.140' },
            {'hostname':'http://netgear.com', 'ip':'http://13.248.140.194' },
            {'hostname':'http://python.org', 'ip':'http://45.55.99.72' },
            {'hostname':'http://yahoo.com', 'ip':'http://72.30.35.9' },
            {'hostname':'http://imgur.com','ip':'http://151.101.56.193' },
            {'hostname':'http://atlassian.com','ip':'http://18.234.32.195' }
        ]

    s = requests.Session()

    while True: 
        for target in urls: 
            # first try to connect to hostname like google.com
            try: 
                timestamp = datetime.now()
                r = s.get(url=target['hostname'], stream=False)
                logging.info(' {} : connected to {} successfully'.format(timestamp, target['hostname']))
            except requests.urllib3.exceptions.NewConnectionError as e:
                logging.warning(' {} : could not connect to {} trying IP address'.format(timestamp, target['hostname']))

                # next, try the IP directly
                try: 
                    timestamp = datetime.now()
                    r = s.get(url=target['ip'], stream=False)
                    logging.info(' {} :\t Connected to {} successfully'.format(timestamp, target['ip']))
                except Exception as e: 
                    logging.warning(' {} :\t Error - could not connect to hostname or IP: {}'.format(timestamp, e))

            sleep(30)

def setup_log():
    # Make a log/ directory in the current working directory
    # if it doesn't exist yet.
    cwd = os.getcwd()

    try: 
        os.mkdir(os.path.join(cwd, 'log'))
    except FileExistsError as e: 
        pass

    date = datetime.today().strftime('%Y-%m-%d')
    logging.basicConfig(filename='log/pingtest-' + date + '.log', level=logging.INFO)

if __name__ == '__main__':
    setup_log()
    main()







