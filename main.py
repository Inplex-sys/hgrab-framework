import sys
import re
import time
import tabulate
import requests
import colored
from colored import stylize
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

params = {
    'counter': {
        'total': 0,
        'found': 0
    }
}

class Main:
    def updateResult():
        while True:
            time.sleep(1)
            print("\033[H\033[2J")
            try:
                hitRate = str(round(params['counter']['found']/params['counter']['total']*100, 2)) + "%"
            except:
                hitRate = "0%"
                pass

            table = [
                ['Total', stylize('Found', colored.fg("green")), stylize('Undetected', colored.fg('red')), 'Hitrate'], 
                [
                    params['counter']['total'], 
                    params['counter']['found'],
                    params['counter']['total'] - params['counter']['found'], 
                    hitRate
                ]
            ]

            print(f"All your results are going to be saved in the file {stylize(f'/root/scan-output/{sys.argv[3]}.txt', colored.fg('wheat_1'), colored.attr('bold'))}\n")
            print(tabulate.tabulate( table, headers='firstrow', tablefmt='fancy_grid'))
            pass
        pass

    def saveHost(host):
        with open(f'/root/scan-output/{sys.argv[3]}.txt' , 'a') as file:
            file.write(host + "\n")
            file.close()
            pass
        pass

    def httpRequest(sheme, host, port, path):
        try:
            headers = {
                "accept": "*/*",
                "accept-encoding": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "sec-ch-ua": '"Google Chrome";v="96", "Chromium";v="96", ";Not A Brand";v="99"',
                "sec-ch-ua-mobile": '?0',
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": 'empty',
                "sec-fetch-mode": 'cors',
                "sec-fetch-site": 'same-origin',
                "user-agent": "Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)"
            }

            if port == "80" or port == "443":
                url = "{}://{}/{}".format(sheme, host, path)
            else:
                url = "{}://{}:{}/{}".format(sheme, host, port, path)
                pass

            httpObject = requests.get(url, headers=headers, verify=False, timeout=5)

            params['counter']['total'] += 1
            return httpObject
        except:
            return False
            pass
        pass

class Scan:
    def run( host ):
        sheme = sys.argv[1]
        port = sys.argv[2]
        software = sys.argv[3]

        if sys.argv[3] == "unifi":
            httpResponse = Main.httpRequest(sheme, host, port, "manage/account/login")
            if httpResponse == False:
                return False
                pass

            if "UniFi Network" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass
        elif sys.argv[3] == "vmware-vcenter":
            httpResponse = Main.httpRequest(sheme, host, port, "")
            if httpResponse == False:
                return False
                pass

            if "ID_VC_Welcome" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass
        elif sys.argv[3] == "wso2":
            httpResponse = Main.httpRequest(sheme, host, port, "publisher/site/pages/login.jag")
            if httpResponse == False:
                return False
                pass

            if 'server' not in httpResponse.headers.keys():
                return False
                pass

            if "WSO2" in httpResponse.headers['server']:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass   
        elif sys.argv[3] == "confluence":
            httpResponse = Main.httpRequest(sheme, host, port, "login.action")
            if httpResponse == False:
                return False
                pass

            if "ajs-keyboardshortcut-hash" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass
        elif sys.argv[3] == "bitbucket":
            httpResponse = Main.httpRequest(sheme, host, port, "rest/api/latest/repos")
            if httpResponse == False:
                return False
                pass
            
            try:
                if "size" in httpResponse.json().keys():
                    if httpResponse.json()['size'] != 0:
                        params['counter']['found'] += 1
                        Main.saveHost(host)
                        pass
                    pass
            except:
                pass
            pass
        elif sys.argv[3] == "apache-nifi":
            httpResponse = Main.httpRequest(sheme, host, port, "")
            if httpResponse == False:
                return False
                pass

            if "<title>NiFi</title>" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass
        elif sys.argv[3] == "laravel":
            httpResponse = Main.httpRequest(sheme, host, port, "")
            if httpResponse == False:
                return False
                pass

            if "<title>Laravel</title>" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass
        elif sys.argv[3] == "zimbra":
            httpResponse = Main.httpRequest(sheme, host, port, "")
            if httpResponse == False:
                return False
                pass

            if "<title>Zimbra Web Client Sign In</title>" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass        
        elif sys.argv[3] == "gitlab":
            httpResponse = Main.httpRequest(sheme, host, port, "users/sign_in")
            if httpResponse == False:
                return False
                pass

            if ">About GitLab<" in httpResponse.text:
                params['counter']['found'] += 1
                Main.saveHost(host)
                pass
            pass
        else:
            print("Unknown software : " + str(sys.argv[3]))
            sys.exit(0)
        pass

def main():
    global params


    if len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(            
                "\n"
                "Usage: %s <http/https> <port> <software>\n"
                "\n"
                "   -h, --help      display this help\n"
                "   -v, --version   print version information\n"
                "   -ls --list      list of known software for scanning"
            % sys.argv[0])
            sys.exit(0)
        elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
            print(
                "Hgrab version 1.0.4 ( https://github.com/Inplex-sys/hgrab )\n"
                "Platform: x86_64-python3-pc-linux-gnu"
            )
            sys.exit(0)
        elif sys.argv[1] == "-ls" or sys.argv[1] == "--list":
            print(            
                "\n"
                "Known software for scanning : \n"
                "\n"
                "       vmware-vcenter - VMWare vCenter is a web application that provides a unified interface for managing a virtualized environment.\n"
                "       apache-nifi - Apache NiFi supports powerful and scalable directed graphs of data routing, transformation, and system mediation logic.\n"
                "       confluence - Atlassian Confluence is a Team Workspace Where Knowledge & Collaboration Meet.\n"
                "       gitlab - GitLab that is used for version control and project management.\n"
                "       unifi - Ubiquiti Unifi is a powerful wifi repeater.\n"
                "       wso2 - WSO2's first product was code-named Tungsten, and was meant for the development of web applications.\n"
                "       laravel - Laravel is a PHP web application framework with expressive, elegant syntax.\n"
                "       bitbucket - Bitbucket is a web-based version control repository hosting service owned by Atlassian.\n"
                "       zimbra - Zimbra is a web-based email and collaboration platform developed by Synacor."
            )
            sys.exit(0)
            pass
        pass

    if len(sys.argv) < 3:
        print(            
            "\n"
            "Usage: %s <http/https> <port> <software>\n"
            "\n"
            "   -h, --help      display this help\n"
            "   -v, --version   print version information\n"
            "   -ls --list      list of available software for scanning\n"
        % sys.argv[0])
        sys.exit(0)
        pass

    # Starting the result pusher thread
    threading.Thread(target=Main.updateResult).start()

    for line in sys.stdin:
        ipAdress = re.findall(re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'), line)
        if len(ipAdress) != 0:
            threading.Thread(target=Scan.run, args=[ipAdress[0]]).start()
            pass
        pass
    pass

if __name__ == "__main__":
    main()
    pass
