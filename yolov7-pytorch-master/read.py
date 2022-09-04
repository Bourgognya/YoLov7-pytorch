path = 'output.txt'
f = open(path, 'r')
i,num=0,0
for line in f.readlines():
    print(line)
    num+=int(line)*(10**(2-i))
    i+=1
print(num,"g")
f.close()