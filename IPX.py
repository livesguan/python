#!/usr/bin/env python
# coding: utf-8

import struct
from socket import gethostbyname
from socket import inet_aton
import os
import functools

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)

dat = ""
offset = 0
index = 0

def load(file):
    global dat,offset,index
    try:
        with open(os.path.join(os.path.dirname(__file__), file), "rb") as f:
            dat = f.read()
            offset, = _unpack_N(dat[:4])
            index = dat[4:offset]
    except:
        print "cannot open file 17monipdb.dat"
        exit(0)

def find(ip):
    nip = inet_aton(ip)
    ipdot = ip.split('.')
    if int(ipdot[0]) < 0 or int(ipdot[0]) > 255 or len(ipdot) != 4:
        return "N/A"

    tmp_offset = (int(ipdot[0]) * 256 + int(ipdot[1])) * 4
    start, = _unpack_V(index[tmp_offset:tmp_offset + 4])

    index_offset = index_length = -1
    max_comp_len = offset - 262144 - 4
    start = start * 9 + 262144

    while start < max_comp_len:
        if index[start:start + 4] >= nip:
            index_offset, = _unpack_V(index[start + 4:start + 7] + chr(0).encode('utf-8'))
            index_length, = _unpack_C(index[start + 8:start + 9])
            break
        start += 9

    if index_offset == 0:
        return "N/A"

    res_offset = offset + index_offset - 262144
    return dat[res_offset:res_offset + index_length].decode('utf-8')