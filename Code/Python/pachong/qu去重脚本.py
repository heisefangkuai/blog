import os

def find():
    file = open("./txt/zcjun.txt","r")
    data = list(set(file))
    print(data)
    path = os.getcwd() + '\\txt'
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
    fp = open(".\\txt\\zcjun1.txt",'w+')
    for i in data:
        fp.write(i)
        # fp.write(i+'\r')
    fp.close()

def findDuo(file_dir):
    ok = set()
    find = os.listdir(file_dir)
    for x in find:
        f = open(r"./txt/" + x ,"r")
        for line in f:
            ok.add(str(line.strip()))
    fp = open(".\\txt\\ok.txt",'w+')
    ok = sorted(ok)
    for i in ok:
        fp.write(i+'\n')
    fp.close()



findDuo('./txt')