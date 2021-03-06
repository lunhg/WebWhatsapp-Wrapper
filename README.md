<img alt="Logo" src="https://github.com/Tobaloidee/WebWhatsapp-Wrapper/blob/master/docs/logo/logotype-a-04.png">

## (Based on web.whatsapp.com)
[![PyPI version](https://badge.fury.io/py/webwhatsapi.svg)](https://badge.fury.io/py/webwhatsapi)
[![Firefox version](https://img.shields.io/badge/Firefox-58.0.2-green.svg)]()
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors)

## What is it?
This package is used to provide a python interface for interacting with WhatsAPP Web to send and receive Whatsapp messages.
It is based on the official Whatsapp Web Browser Application and uses Selenium browser automation to communicate with Whatsapp Web.

## Traefik installation

Este repositório é um fork visando a fácil implementação de dois microserviços docker. Para habilitá-los em um _load balancer_ como [Traefik](https://docs.traefik.io/), estas imagens devem ser extendidas ou referenciadas emtro arquivo docker.

Para fins de praticidade, clone este repositório na mesma pasta onde estiver contida a pasta com o código fonte de seu servidor principal.

```
$ cd /home/user/projeto
$ ls -la
drwxrwxr-x    7 user user     4096 Jan 31 00:00 servidor
$ git clone https://github.com/lunhg/WebWhatsapp-Wrapper
$ cd WebWhatsapp-Wrapper
$ git add remote git@gitlab:install/whatsapp.git
$ ls -la
drwxrwxr-x    7 user user     4096 Jan 31 00:00 servidor
drwxrwxr-x    7 user user     4096 Jan 31 00:00 WebWhatsapp
```

Em seu servidor principal, sejam `servidor/docker-compose.yml` o arquivo de configuração do `docker-compose` e `.env` um arquivo de configuração das variáveis de ambiente:

```
# projeto/servidor/docker-compose.yml
# Traefik and containers should have same version
version: '2' 

# Create a network for your selenium
networks:
  selenium:
    ipam:
      driver: default
      config:
      - subnet:  10.0.0.0/<n>
  
 services:
 
    # Load balancer, if you want to add another services and customize your bot, like a database, s3, mailer, etc...
    traefik:
        extends:
            file: ../loadbalancer/docker-compose.yml
            service: traefik
        ports:
            - 80:80/tcp
            - 8080:8080/tcp
            - 443:443/tcp
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock:ro
        labels:
            traefik.frontend.rule: Host:$__tr__
            traefik.alias: traefik
            traefik.port: '8080'
            traefik.enable: 'true'
        networks:
            selenium:
              ipv4_address: 10.0.0.<n>
    
    # The selenium playground
    __wa__:
        extends:
            file: ../WebWhatsapp-Wrapper/docker-compose.yml
            service: $__wa__service
        ports:
            - "4444:4444"
            - "5900:5900"
        volumes:
            - shm_data:/dev/shm
        labels:
            traefik.docker.network: selenium
            traefik.frontend.rule: Host:$__wa__
            traefik.port: '4444'
            traefik.enable: 'true'
        networks:
            selenium:

    # The python bot
    wa:
        extends:
            file: ../WebWhatsapp-Wrapper/docker-compose.yml
            service: whatsapp
        environment:
            - "SELENIUM=https://$__wa__/wd/hub"
        volumes:
            - "wa_data:/home/$username/whatsapp"
        networks:
            minharede: 
        depends_on:
          - __wa__

# =======
# VOLUMES
# =======
volumes:
    wa_data:
    shm_data:
```

E agora `.env`, que conterá as variáveis de ambiente específicas para sua máquina, que definem os domínios de serviço, 
usuário dos containers e tipo de serviço selenium executado (por enquanto, apenas firefox suportado).

```
# services
__tr__=lb.hostname.domain
__wa__=sel.hostname.domain

# projeto/servidor/.env
# User is seluser and pwd is secret. Maybe you can change in Dockerfiles
username=seluser
pwd=secret

# TODO create others seleniums like Dockerfile.chrome...
__wa__service='firefox'
```

Agora é só executar o `docker-compose`no seu servidor principal:

```
$ docker-compose up -d --build --remove-orphans traefik __wa__ wa
```

## Usage for customize python bot

See `lib` directory for how to:

### 0. See the CLI in `lib/wahtsapp.py`:

Usage:

```
python lib/whatsapp.py 
       [-u] --username=<nome> \
       [-l] --logfile=<logfile> \
       [-H] --elastic-search-host <host> \
       [-P] --elastic-search-port <port>
```

#### 0.1 See API for CLI in `lib/bot.py`:

```
import bot
b = bot.Bot(<username>, <profile>, <elSearch>, <logfile>)
b.run()
```

- `<username>`: `String` containing the name of bot;
- `<profile>`: `String` containing the full path of profile;
- `<elSearch>`: `Array<Dictionary>` containing configurations for ech server (default: `[{host: 'localhost', port:9200}]`);
- `<logfile>`: `String` containing the full path of a log file for our bot.
### 1. Import library

    from webwhatsapi import WhatsAPIDriver

### 2. Instantiate driver and set username

    driver = WhatsAPIDriver(username="mkhase")

Possible arguments for constructor:

- client : Type of browser. The default is Firefox, but Chrome and Remote is supported too. See sample directory for remote examples.
- username : Can be any value.
- proxy: The proxy server to configure selenium to. Format is "<proxy>:<portnumber>"
- command_executor: Passed directly as an argument to Remote Selenium. Ignore if not using it. See sample directory for remote examples. 
- loadstyles: Default is False. If True, it will load the styling in the browser.
- profile: Pass the full path to the profile to load it. Profile folder will be end in ".default". For persistent login, open a normal firefox tab, log in to whatsapp, then pass the profile as an argument.

### 3. Use a function to save the QR code in a file, for remote clients, so that you can access them easily. Scan the QR code either from the file, or directly from the client to log in.

    driver.get_qr()

### 4. In case the QR code expires, you can use the reload_qr function to reload it

    driver.reload_qr()

### 5. Viewing unread messages

    driver.view_unread()

### 6. Viewing all contacts

    driver.get_all_chats()

### 7. To send a message, get a Contact object, and call the send_message function with the message.

    <Contact Object>.send_message("Hello")

### 8. Sending a message to an ID, whether a contact or not.

    driver.send_message_to_id(id, message)

## Code Documentation
https://webwhatsapi.readthedocs.io/en/latest/

## Limitation
Phone needs to manually scan the QR Code from Whatsapp Web. Phone has to be on and connected to the internet.

# Capabilities
 - Read recent messages
 - Get unread messages
 - Send text messages
 - Get List of Contacts
 - Get List of Groups
 - Get information about Groups
 - Get various events. For example: Leaving, Joining, Missed Call etc.
 - Download media messages
 - Get List of common groups
 - Asyncio driver version

## Note
There are issues with asynchronous calls in Chrome. Primary support of this api is for firefox. If something doesn't work in chrome, please try firefox.

### Known issues with chrome:
 - Group Metadata
 
### For more queries, contact: mukulhase@gmail.com

## Contribute
Contributing is simple as cloning, making changes and submitting a pull request.
If you would like to contribute, here are a few starters:
- Bug Hunts
- More sorts of examples
- Additional features/ More integrations (This api has the minimum amount, but I don't mind having more data accessible to users)
- Create an env/vagrant box to make it easy for others to contribute. (At the moment, all I have is a requirements.txt
- Phantom JS support

## Legal
This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by WhatsApp or any of its affiliates or subsidiaries. This is an independent and unofficial software. Use at your own risk.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification. Contributions of any kind welcome!
