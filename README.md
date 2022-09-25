# Hgrab

### Additional Informations
 - Not using too much bandwith
 - multiple software support

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

## Avaible software (we will add custom query in the future)
```
Known software for scanning :

       vmware-vcenter - VMWare vCenter is a web application that provides a unified interface for managing a virtualized environment.
       apache-nifi - Apache NiFi supports powerful and scalable directed graphs of data routing, transformation, and system mediation logic.
       confluence - Atlassian Confluence is a Team Workspace Where Knowledge & Collaboration Meet.
       gitlab - GitLab that is used for version control and project management.
       unifi - Ubiquiti Unifi is a powerful wifi repeater.
       wso2 - WSO2's first product was code-named Tungsten, and was meant for the development of web applications.
       laravel - Laravel is a PHP web application framework with expressive, elegant syntax.
       bitbucket - Bitbucket is a web-based version control repository hosting service owned by Atlassian.
```

### Using hgrab with **zmap** for scanning vmware-vcenter targets on **tcp/443**
`zmap -p 443 | python3 ./main.py http 443 vmware-vcenter`
![image](https://user-images.githubusercontent.com/69421356/189482048-43bbe0d5-db69-45e4-b665-db1360b7626d.png)
