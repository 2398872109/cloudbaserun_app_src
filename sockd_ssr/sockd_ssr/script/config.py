#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import sys
import logging

logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s: %(message)s')

ciphers_list = {
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

protocol_list = {
    "origin",
    "auth_aes128_md5", 
    "auth_aes128_sha1", 
    "auth_sha1_v4",
    "auth_sha1_v4_compatible",
    "auth_chain_a", 
    "auth_chain_b", 
    "auth_chain_c", 
    "auth_chain_d", 
    "auth_chain_e",
    "auth_chain_f",
    
}

obfs_list = {
    "plain",
    "http_simple",
    "http_simple_compatible",
    "http_post",
    "http_post_compatible",
    "random_head",
    "random_head_compatible",
    "tls1.2_ticket_auth",
    "tls1.2_ticket_auth_compatible",
    "tls1.2_ticket_fastauth",
    "tls1.2_ticket_fastauth_compatible",
}


ENVConfig = {
    "SERVER_PORT":"server_port",
    "METHOD":"method",
    "PASSWORD":"password",
    "PROTOCOL":"protocol",
    "PROTOCOL_PARAM":"protocol_param",
    "OBFS":"obfs",
    "OBFS_PARAM":"obfs_param"
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
    for key in ENVConfig.keys():
        if key in os.environ.keys():
            config[ENVConfig[key]] = os.environ.get(key);
            if key == "METHOD":
                cipher_check(config)
            if key == "PROTOCOL":
                protocol_check(config)
            if key == "OBFS":
                obfs_check(config)
    return config

def cipher_check(config):
    if config["method"] not in ciphers_list:
        logging.error('Method not support: %s', str(config["method"]))
        sys.exit(1)
    return config


def protocol_check(config):
    if config["protocol"] not in protocol_list:
        logging.error('Protocol not support: %s', str(config["protocol"]))
        sys.exit(1)
    return config


def obfs_check(config):
    if config["obfs"] not in obfs_list:
        logging.error('OBFS not support: %s', str(config["obfs"]))
        sys.exit(1)
    return config


if __name__ == "__main__":
    config_file_path = "/home/config.json"
    config_env = read_config_from_env()
    config_file = load_config(config_file_path)
    for key in config_file.keys():
        if key in config_env.keys():
            config_file[key] = config_env[key]
    print("generate config:",config_file)
    write_config(config_file_path, config_file)
    import subprocess
    subprocess.call("/home/shadowsocks/server.py -c /home/config.json", shell=True)