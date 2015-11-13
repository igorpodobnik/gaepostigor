__author__ = 'igorpodobnik'



def matematika(a,b,oper):
    if a.isdigit():
        a=int(a)
    else:
        a=0
    if b.isdigit():
        b=int(b)
    else:
        a=b
    if oper == "+":
        rez = a+b
    elif oper == "-":
        rez = a-b
    elif oper == "*":
        rez = a*b
    elif oper == "/":
        rez = (a+0.0)/(b+0.0)
    else:
        rez = "neveljavni operator!"
    return rez

def pretvorba(a,b,c):
    rez="Ni se zgodilo"
    if a.isdigit():
        a=int(a)
    else:
        rez = "Vnesi stevilko!!!"
    if b == "s":
        if c == "min":
            min = a / 60
            ostanek = a - (min *60)
            rez = str(min)+ " min in "+str(ostanek)+" sekund"
    elif b == "km":
        if c == "mi":
            vmestno = a*0.621
            rez = str(vmestno) + " milj"
    else:
        rez = "dej vnesi s/min ali pa km/mi"
    return rez

def randomm(stevilka):
    if stevilka.isdigit():
        stevilka=int(stevilka)
        if stevilka<glavna_stevilka:
            tekst = "Premajhna"
        elif stevilka>glavna_stevilka:
            tekst = "Prevelika"
        else:
            tekst = "--- Zmaga!!! ---"
    else:
        tekst="Vnesi stevilko"
    return tekst