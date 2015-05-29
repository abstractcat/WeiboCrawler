__author__ = 'chi'

def main():
    f=open('pin_300.txt')
    lines=f.readlines()
    f.close()
    lines=map(lambda x:x.split('\t'),lines)
    pins=map(lambda x:x[0],lines)
    letters=map(lambda x:x[1].strip().lower(),lines)

    ld=dict()
    for letter in letters:
        for c in letter:
            count=ld.get(c,0)
            ld[c]=count+1

    for c in ld:
        print(c+':'+str(ld[c]))

if __name__ == '__main__':
    main()
