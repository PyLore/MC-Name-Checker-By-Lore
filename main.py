from requests           import request
from concurrent.futures import ThreadPoolExecutor
from argparse           import ArgumentParser
from random             import choices

from data.theme         import Colors
from data.proxies       import get_proxies

HEADERS = {
    'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection'     : 'close'
}



def main(file: str) -> None:
    global proxies, checked
    proxies = get_proxies(requester=request)
    checked = set()
    file    = open(file).readlines()
    print(f'{Colors.WHITE}Checking {len(file)} names...\n')
    
    with ThreadPoolExecutor(max_workers=600) as executor:
        for source in file:
            if (stripped := source.strip()) in checked:
                continue
            
            executor.submit(mc_checker, stripped)

def mc_checker(username: str) -> None:
    # fun stuff happens here
    while True:
        try:
            proxy = next(proxies)
            resp  = request(
                method  = 'GET',
                url     = f'https://api.mojang.com/users/profiles/minecraft/{username}',
                proxies = {'https': f'http://{proxy}'},
                headers = HEADERS,
                timeout = 4
            ).status_code
        except:
            continue
            
        # If we got a hit.    
        if resp == 204:
           print(f'{Colors.WHITE}[{Colors.LIME}Available{Colors.WHITE}] {Colors.YELLOW}{username:<16}{Colors.WHITE}| {Colors.AQUA}{proxy}') 
        
        checked.add(username)
        break


                
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-l',
        '--list',
        help    ='Name list (ex: names.txt)',
    )
    args = parser.parse_args()

    main(args.list)
