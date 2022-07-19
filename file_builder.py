import sys
import requests
from ruamel.yaml import YAML
import os

yaml = YAML()

def token_change(TOKEN=None):
    from cryptography.fernet import Fernet
    import subprocess

    if TOKEN == None:
        TOKEN = input('Enter the bot token: ')

    key = Fernet.generate_key()
    with open("resources/.key.yml", 'w') as file:
        yaml.dump({"key": key}, file)

    with open("resources/.token.yml", 'w') as file:
        yaml.dump({"token": Fernet(key).encrypt(TOKEN.encode())}, file)

    del Fernet
    del subprocess

keey = b'xZ2ulKiI1ZjYaFtwtt09B-gkEsnzelg7vud_9I62opI='
def config(regen=False, check=False, TOKEN=None,
    bot_owners_list=None, bot_owners_message_enabled=None,
    reddit_login_client_id=None, reddit_login_client_secret=None, reddit_login_user_agent=None,
    modules_add=None, modules_memes=None, modules_nsfw=None,
           ):

    if regen == True:
        version = yaml.load(open('resources/.version.yml', 'r')).get("version")
        url = f'https://raw.githubusercontent.com/kchulka/p-bot/{version}/config/config.yml'
        config_request = requests.get(url, allow_redirects=True)
        open('config/config.yml', 'wb').write(config_request.content)

    else:
        new_config = yaml.load(open('config/config.yml', 'r'))

        if TOKEN != None or new_config['TOKEN'] != ' ':
            if new_config['TOKEN'] != ' ':
                TOKEN = new_config['TOKEN']
            token_change(TOKEN)


        new_config['TOKEN'] = ' '

        if bot_owners_list != None:
            new_config['bot_owners']['list'] = bot_owners_list

        if bot_owners_message_enabled != None:
            new_config['bot_owners']['message_enabled'] = bot_owners_message_enabled

        if reddit_login_client_id != None:
            new_config['reddit_login']['client_id'] = reddit_login_client_id

        if reddit_login_client_secret != None:
            new_config['reddit_login']['client_secret'] = reddit_login_client_secret

        if reddit_login_user_agent != None:
            new_config['reddit_login']['user_agent'] = reddit_login_user_agent

        if modules_add != None:
            for module in modules_add:
                new_config['modules'][f'{module}'] = "disabled"


        if modules_memes != None:
            new_config['modules']['memes'] = modules_memes

        if modules_nsfw != None:
            new_config['modules']['nsfw'] = modules_nsfw

        with open("config/config.yml", 'w') as file:
            yaml.dump(new_config, file)

def bot():
    version = yaml.load(open('resources/.version.yml', 'r')).get("version")
    url = f'https://raw.githubusercontent.com/kchulka/p-bot/{version}/bot.py'
    config_request = requests.get(url, allow_redirects=True)
    open('bot.py', 'wb').write(config_request.content)

"""
    jak se dostat k zasifrovanymu tokenu
    
    secretkey = yaml.load(open('resources/key.yml', 'r'), Loader=Loader).get("key")
    # print(f"klíč2: {secretkey}")

    TOKEN = yaml.load(open('resources/token.yml', 'r'), Loader=Loader).get("token")
    print(TOKEN)
    TOKEN = Fernet(secretkey).decrypt(yaml.load(open('resources/token.yml', 'r'), Loader=Loader).get("token")).decode(
        'utf-8')

    TOKEN = Fernet(secretkey).decrypt(
        yaml.load(open(f"{yaml.load(open('config/config.yml', 'r'), Loader=Loader).get('Token_path')}", 'r'),
                  Loader=Loader).get("token")).decode('utf-8')

    print(TOKEN)"""



"""


#This part of the config is dedicated to usage logging.
default_logging:
  #Command usage will save most of the data about the message the bot sent.
    #  enabled: True / False                - If you want to log some information about the bot usage
    #  method: webhook / file / both        - This determines where are the logs stored -- only webhook is now working
    #  webhook: link
  command_usage:
    enabled: false
    method: ' '
    webhook: ' '






"""