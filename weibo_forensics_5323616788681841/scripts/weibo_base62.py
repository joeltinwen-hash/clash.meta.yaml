#!/usr/bin/env python3
ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def int_to_base62(n:int)->str:
    if n == 0: return '0'
    s=''
    while n:
        n,r=divmod(n,62); s=ALPHABET[r]+s
    return s

def mid_to_url(mid:str)->str:
    mid=str(mid)[::-1]
    parts=[mid[i:i+7][::-1] for i in range(0,len(mid),7)]
    out=[]
    for i,p in enumerate(parts):
        b=int_to_base62(int(p))
        if i < len(parts)-1: b=b.zfill(4)
        out.append(b)
    return ''.join(out[::-1])
if __name__=='__main__':
    import sys
    for x in sys.argv[1:]: print(x, mid_to_url(x))
