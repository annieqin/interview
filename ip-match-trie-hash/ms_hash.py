# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import sys
import re

content = sys.stdin.readlines()
nrules, nips = [int(i) for i in content[0].split()]
rules = content[1:1+nrules]
ips = content[1+nrules:1+nrules+nips]

table = [[] for _ in range(11)]
count = 0


def hash_fun(x):
    return x % 10


def insert(ip_input, value):
    table[hash_fun(hash(ip_input))].append(value)


for rule in rules:
    count += 1
    re_type = re.search('allow|deny', rule)
    if re_type:
        type = re_type.group()
        re_ip = re.search('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}[\s\S]*', rule)
        if re_ip:
            ip = re_ip.group()
            if '/' in ip:
                mask = int(ip.split('/')[1])
            else:
                mask = 32
            ip_bit = ''.join([bin(int(i))[2:].zfill(8) for i in ip.split('/')[0].split('.')])[:mask]
            insert(ip, (count, type, ip_bit))

ips_bit = []
for i in ips:
    ips_bit.append(''.join([bin(int(k))[2:].zfill(8) for k in i.split('.')]))


for ip in ips_bit:
    result = []
    min_id = float("inf")
    min_match = None
    for rules in table:
        for rule in rules:
            re_match = re.match(rule[2], ip)
            if re_match:
                result.append(rule)
    if result:
        for i in result:
            if i[0] < min_id:
                min_id = i[0]
                min_match = i
        print 'YES' if min_match[1] == 'allow' else 'NO'
    else:
        print 'YES'

