# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import sys

content = sys.stdin.readlines()
ngifts, ncoupons = [int(i) for i in content[0].split()]

need = []
value = []

opt = {}


for i in range(1, ngifts+1):
    need.append(int(content[i].split()[0]))
    value.append(int(content[i].split()[1]))


def cal(m, n):
    if n >= ngifts or m <= 0:
        return 0
    if opt.get((m, n)):
        return opt[(m, n)]
    else:
        ret = 0
        for k in range(2):
            temp = cal(m - k*need[n], n+1)
            if m - k*need[n] >= 0:
                temp += value[n]*k
                if temp > ret:
                   ret = temp
        opt[(m, n)] = ret
        return ret

print cal(ncoupons, 0)
