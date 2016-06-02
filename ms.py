# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import re
import sys
import datetime
content = sys.stdin.readlines()
nrules, nips = [int(i) for i in content[0].split()]
lines = content[1:1+nrules]
ips = content[1+nrules:1+nrules+nips]


def match(line, rules):
    re_type = re.search('allow|deny', line)
    if re_type:
        type = re_type.group()
        re_rule = re.search('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}[\s\S]*', line)
        if re_rule:
            rule = re_rule.group()
            # re_dot = re.compile('\.')
            # ip = re_dot.sub('', ip)
            temp = rule.split('/')
            ip = temp[0].split('.')
            ip_bin = [bin(int(i))[2:].zfill(8) for i in ip]
            if rule.find('/') == -1: #  完全匹配
                ip_bin = ''.join(ip_bin)
                rules.append((32, ip_bin, type))
            else: #  不完全匹配
                mask = int(temp[1])
                ip_bin = ''.join(ip_bin)[:mask]
                rules.append((mask, ip_bin, type))
    print rules
    return

start = datetime.datetime.now()
rules = []
for line in lines:
    match(line, rules)

for ip in ips:
    match_flag = 0
    # re_dot = re.compile('\.')
    # ip = int(re_dot.sub('', ip))

    # rule: (mask, ip_bin, type)
    for rule in rules:
        mid = ip.split('.')
        mid = [bin(int(i))[2:].zfill(8) for i in mid]
        mid = ''.join(mid)[:rule[0]]
        if mid == rule[1]:
            if rule[2] == 'allow':
                print 'yes'
                match_flag = 1
                break
            elif rule[2] == 'deny':
                print 'no'
                match_flag = 1
                break
    if not match_flag:
        print 'yes'
end = datetime.datetime.now()

print end-start