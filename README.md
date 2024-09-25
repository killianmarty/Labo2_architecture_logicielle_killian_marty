# Architeture des logiciels : Laboratoire 2

## 1. Déploiement avec distribution de charge

1.Pour ce laboratoire, j'utilise un environnement virtuel python pour installer flask et exécuter l'application :

```bash
    python.exe -m venv nom_environnement
    cd nom_environnement
    .\Scripts\activate
    pip install flask
    py app_KM.py
```

Je peux également créer un fichier requirements.txt pour donner mes dépendances au membre B:

```bash
pip freeze > requirements.txt
```

3.Pour l'adresse IP, au lieu de la hardcoder, je la récupère grâce au package "socket" :

```python
import socket

def hello_world():
    return "<h2>Hello, World! From KM: " + socket.gethostbyname(socket.gethostname()) + "</h2>"
```

5.Le navigateur affiche bien notre "hello world".

![](captures/Helloworld.PNG)

6.Si le serveur est arrêté, la page est inaccessible.

![](captures/Unreachableserver.PNG)

8.Note: pour partager mon code sur github avec le membre B, je créer un fichier .gitignore afin d'aviter de pousser l'environnement virtuel sur la branche distante:

```gitignore
/Include/
/Scripts/
/Lib/
/pyvenv.cfg
/pip-selfcheck.json
```

9.Je clone le repo git du membre B, (et je lui créer un environnement virtuel python), je modifie son code pour lui attribuer le port 3001.


13.Les deux applications fonctionnent bien.

14.Voici la nouvelle configuration de nginx avec IP_A: 172.16.14.35 et IP_B: 172.16.14.36 (nginx.conf):

```conf

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;
    upstream labcluster {

      server 172.16.14.35:3000;
      server 172.16.14.36:3001;

    }
    server {
      listen 8181 default_server;
      #listen [::]:8181 default_server;
      #root /var/www/html;
      #server_name _;

      location / {
        proxy_pass http://labcluster;
        try_files $uri $uri/ =404;
      }


      #location /labapp {
       # proxy_pass http://labcluster/labapp;
      #}
      

}


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
```

16.Une fois nginx configuré, en rechargant la page IP_MEMBRE_A:8181, on voit que la page du membre A s'affiche, mais parfois avec l'adresse IP du membre B. C'est dû à nginx qui redirige les requêtes sur plusieurs serveurs (les machines du membre A et B):

![](captures/serveur_machineA.png)

![](captures/serveur_machineB.png)

17.En arrêtant le serveur A sur la machine A, l'application n'est plus accessible à l'adresse IP_A:3000:

![](captures/Unreachableserver.PNG)

Cependant, l'application est toujours accessible sur le port 8181, mais l'adresse affichée est uniquement l'IP_B. En effet, nginx détecte que la machine A ne répond plus aux requêtes et redirige donc tout vers la machine B:

![](captures/serveur_machineB.png)