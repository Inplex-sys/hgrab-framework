# Hgrab

### Additional Informations
 - Not using too much bandwith
 - multiple software

### Installation
Install the app on the server
```sh
user@domain:~# git clone https://github.com/Inplex-sys/hgrab.git
user@domain:~# cd ./hgrab/
user@domain:~# pip3 install requests
user@domain:~# mkdir ./scan-output/
user@domain:~# cat ./your-file.txt | python3 ./main.py <http/https> <port> <software>
```

## Help banner
```
Usage: main.py <http/https> <port> <software>

   -h, --help      display this help
   -v, --version   print version information
   -ls --list      list of available software for scanning
```

### Using hgrab with **zmap** for scanning vmware-vcenter targets on **tcp/443**
`zmap -p 443 | python3 ./main.py http 443 vmware-vcenter`
![image](https://user-images.githubusercontent.com/69421356/189482048-43bbe0d5-db69-45e4-b665-db1360b7626d.png)
