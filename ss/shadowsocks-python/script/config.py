#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import sys
import logging

logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s: %(message)s')

ciphers = {
    "aes-256-gcm",
    "aes-192-gcm",
    "aes-128-gcm",
    "aes-256-ctr",
    "aes-192-ctr",
    "aes-128-ctr",
    "aes-256-cfb",
    "aes-192-cfb",
    "aes-128-cfb",
    "camellia-128-cfb",
    "camellia-192-cfb",
    "camellia-256-cfb",
    "chacha20-ietf-poly1305",
    "chacha20-ietf",
    "chacha20",
    "rc4-md5",
}

ENVConfig = {
    "PORT",
    "METHOD",
    "PASSWORD"
}

def load_config(file_path):
    config = {}
    if os.path.exists(file_path) == False:
        return None
    with open(file_path, 'r') as f:
        try:
            config = json.load(f)
        except ValueError as e:
            logging.error('found an error in reading config.json: %s', str(e))
            sys.exit(1)
    return config

def write_config(file_path,config):
    with open(file_path, 'w+') as f:
        try:
            print("write config",config)
            json.dump(config,f)
        except ValueError as e:
            logging.error('found an error in writing config.json: %s', str(e))
            sys.exit(1)

def read_config_from_env():
    config = {}
    if "SERVER_PORT" in os.environ.keys():
        config["server_port"] = os.environ.get("SERVER_PORT");
    if "METHOD" in os.environ.keys():
        config["method"] = os.environ.get("METHOD");
        cipher_check(config)
    if "PASSWORD" in os.environ.keys():
        config["password"] = os.environ.get("PASSWORD");
    return config

def cipher_check(config):
    if config["method"] not in ciphers:
        logging.error('Method not support: %s', str(config["method"]))
        sys.exit(1)
    return config

def parse_json_in_str(data):
    return json.loads(data)

if __name__ == "__main__":
    config_file_path = "/home/config.json"
    config_from_env = read_config_from_env()
    config_from_file = load_config(config_file_path)
    for key in config_from_file.keys():
        if key in config_from_env.keys():
            config_from_file[key] = config_from_env[key]
    print("final config file:",config_from_file)
    write_config(config_file_path, config_from_file)
    import subprocess
    subprocess.call("ssserver -c "+config_file_path, shell=True)