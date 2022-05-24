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
    with open(file_path, 'rb') as f:
        try:
            config = parse_json_in_str(remove_comment(f.read().decode('utf8')))
        except ValueError as e:
            logging.error('found an error in reading config.json: %s', str(e))
            sys.exit(1)
    return config

def write_config(file_path,config):
    if os.path.exists(file_path) == False:
        logging.error('config.json not exist: %s', str(e))
        sys.exit(1)
    with open(file_path, 'rb') as f:
        try:
            json.dump(config,f)
        except ValueError as e:
            logging.error('found an error in writing config.json: %s', str(e))
            sys.exit(1)

def read_config_from_env():
    config = {}
    if "PORT" in os.environ.keys():
        config["server_port"] = os.environ.get("PORT");
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



def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

class JSFormat:
    def __init__(self):
        self.state = 0

    def push(self, ch):
        ch = ord(ch)
        if self.state == 0:
            if ch == ord('"'):
                self.state = 1
                return to_str(chr(ch))
            elif ch == ord('/'):
                self.state = 3
            else:
                return to_str(chr(ch))
        elif self.state == 1:
            if ch == ord('"'):
                self.state = 0
                return to_str(chr(ch))
            elif ch == ord('\\'):
                self.state = 2
            return to_str(chr(ch))
        elif self.state == 2:
            self.state = 1
            if ch == ord('"'):
                return to_str(chr(ch))
            return "\\" + to_str(chr(ch))
        elif self.state == 3:
            if ch == ord('/'):
                self.state = 4
            else:
                return "/" + to_str(chr(ch))
        elif self.state == 4:
            if ch == ord('\n'):
                self.state = 0
                return "\n"
        return ""

def remove_comment(json):
    fmt = JSFormat()
    return "".join([fmt.push(c) for c in json])

def parse_json_in_str(data):
    # parse json and convert everything from unicode to str
    return json.loads(data, object_hook=_decode_dict)


if __name__ == "__main__":
    config_file_path = "/etc/shadowsocks-python/config.json"
    config_env = read_config_from_env()
    config_file = load_config(config_file_path)
    for key in config_file.keys():
        if key in config_env.keys():
            config_file[key] = config_env[key]
    print(config_file)
    write_config(config_file_path, config_file)
    import subprocess
    subprocess.call("ssserver -c /home/config.json", shell=True)