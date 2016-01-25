import re

ls = open("weapons_big.txt").readlines()
x = r"talents"
all = set()
for l in ls:
    #l = re.sub(r" \([+-][0-9]+,[ ]*[0-9]+d[0-9]+[+-]*[0-9]*\)","",l)
    if (not (l in all or re.search(x,l))):
        all.add(l)
        print(l.strip())
