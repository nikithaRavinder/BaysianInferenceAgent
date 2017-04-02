import sys

def enumerationAsk(X, e, bayesNet, vars, flag):
    QX = {}
    for xi in ['+','-']:
        e[X] = xi
        QX[xi] = enumerateAll(vars, e, bayesNet)
        del e[X]
    if flag == 1:
        return normalize(QX)
    else:
        return (QX)

def enumerateAll(vars, e, bayesNet):
    if len(vars) == 0:
        return 1.0
    Y = vars.pop()
    if Y in e:
        value = probability(Y, e[Y], e, bayesNet) * enumerateAll(vars, e, bayesNet)
        vars.append(Y)
        return value
    else:
        total = 0
        e[Y] = '+'
        total += probability(Y, e[Y], e, bayesNet) * enumerateAll(vars, e, bayesNet)
        e[Y] = '-'
        total += probability(Y, e[Y], e, bayesNet) * enumerateAll(vars, e, bayesNet)
        del e[Y]
        vars.append(Y)
        return total

def normalize(QX):
    total = 0.0
    for value in QX.values():
        total += value
    for key in QX.keys():
        QX[key] /= total
    return QX

def probability(var, value, e, bayesNet):
    parents = bayesNet[var][0]
    if len(parents) == 0:
        PrTrue = bayesNet[var][1][None]
    else:
        parentvals = [e[parent] for parent in parents]
        PrTrue = bayesNet[var][1][tuple(parentvals)]
    if value == '+':
        return PrTrue
    else:
        return 1.0 - PrTrue

def main():
    #fname = sys.argv[1]
    fname = "test2.txt"
    fin = open(fname, "r")
    line = fin.read().splitlines()
    count = int(line[0])
    querylist = []
    for i in range(1,count+1):
        querylist.append(line[i])
    bayesNet = {}
    vars = []
    i = count+1
    while i < len(line):
        parents = []
        node = None
        temp = {}
        if line[i][0].isupper():
            if "|" in line[i]:
                node = line[i].split('|')[0].strip()
                vars.insert(0,node)
                parents = line[i].split('|')[1].strip().split()
            else:
                node = line[i].strip()
                vars.insert(0,node)
        n = len(parents)
        for j in range(1, pow(2,n)+1):
            if line[i+j][0] == "0":
                if "+" in line[i+j] or "-" in line[i+j]:
                    thisline = line[i+j].split()
                    if len(thisline) == 2:
                        temp.update({tuple(thisline[1]):float(thisline[0])})
                    elif len(thisline) == 3:
                        temp.update({tuple(thisline[1]+thisline[2]):float(thisline[0])})
                    elif len(thisline) == 4:
                        temp.update({tuple(thisline[1]+thisline[2]+thisline[3]):float(thisline[0])})
                else:
                    temp = {None:float(line[i+j].strip())}
        i = i+j+2
        bayesNet.update({node:[parents,temp]})

    fop = open("output.txt","w")
    sys.stdout = fop

    for query in querylist:
        X = None
        N = {}
        D = {}
        e = {}
        flag = 0
        multi = False
        Xtype = None

        if "|" in query:
            flag = 1
            first = query.split("|")[0]
            second = query.split("|")[1]
            if ',' in first:
                multi = True
                tmp = first.split(',')
                for idx, each in enumerate(tmp):
                    N.update({tmp[idx].split('=')[0].lstrip('P(').strip(): tmp[idx].split('=')[1].strip()})
            else:
                Xtype = first.split('=')[1]
                X = first.split('=')[0].lstrip('P(').strip()

        else:
            first = []
            second = query

        tmp = second.split(',')
        for idx, each in enumerate(tmp):
            tmp[idx] = each.lstrip('P(').rstrip(')').strip()
            if multi:
                N.update({tmp[idx].split('=')[0].strip(): tmp[idx].split('=')[1].strip()})
                D.update({tmp[idx].split('=')[0].strip(): tmp[idx].split('=')[1].strip()})
            else:
                e.update({tmp[idx].split('=')[0].strip(): tmp[idx].split('=')[1].strip()})

        if multi :
            resN = enumerationAsk(None, N, bayesNet, vars, 0)
            resD = enumerationAsk(None, D, bayesNet, vars, 0)
            print format(resN['+']/resD['+'], '.2f')

        else:
            result = enumerationAsk(X, e, bayesNet, vars, flag)
            if Xtype == ' - ':
                print format(result['-'],'.2f')
            else:
                print format(result['+'],'.2f')

    fin.close()
    fop.close()

if __name__ == '__main__':
    main()