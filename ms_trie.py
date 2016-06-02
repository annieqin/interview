# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import collections
import re
import sys

content = sys.stdin.readlines()
nrules, nips = [int(i) for i in content[0].split()]
rules = content[1:1+nrules]
ips = content[1+nrules:1+nrules+nips]


class TrieNode(object):
    def __init__(self):
        self.is_rule = False
        self.id = 0
        self.type = None
        self.children = collections.defaultdict(TrieNode)
        self.rule = None


class Trie(object):
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def insert(self, rule):
        node = self.root

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

                for bit in ip_bit:
                    node = node.children[bit]

                if not node.is_rule:
                    node.rule = ip_bit
                    node.is_rule = True
                    node.type = type
                    self.size += 1
                    node.id = self.size

    def search(self, ip):
        node = self.root
        ret = []
        if self.root.is_rule:
            ret.append(self.root)

        for bit in ip:
            if bit in node.children:
                if node.children[bit].is_rule:
                    ret.append(node.children[bit])
                node = node.children[bit]
            else:
                break
        return ret if ret else None

    def putout(self, node):
        if node.is_rule:
            print str(node.id)+' '+str(node.type)+' '+str(node.rule)
        for c in node.children:
            self.putout(node.children[c])


trie = Trie()

for r in rules:
    trie.insert(r)

ips_bit = []
for i in ips:
    ips_bit.append(''.join([bin(int(k))[2:].zfill(8) for k in i.split('.')]))

for i in ips_bit:
    matches = trie.search(i)

    if matches:
        min_id = float("inf")
        min_match = None
        for match in matches:
            if match.id < min_id:
                min_id = match.id
                min_match = match
        print 'YES' if min_match.type == 'allow' else 'NO'
    else:
        print 'YES'

# trie.putout(trie.root)

