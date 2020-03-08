from decimal import Decimal

dec = Decimal
degrad = 'deg'
pi = 3.14159265358979323846
terms = dec(9)    #number of terms used for the trig calculations

def version():
    print('numerics.py version 1.0.0')
    print('Packaged with the cubes project')
def mode(modeinput = ''):    #switch between degrees and radians or check the current mode
    global degrad
    if modeinput == 'deg':
        degrad = 'deg'
        return 'deg'
    if modeinput == 'rad':
        degrad = 'rad'
        return 'rad'
    if modeinput == '':
        return degrad
    else:
        return False
        
def accuracy(accinput = ''):
    global terms
    global pi
    if accinput == '':
        return terms
    terms = dec(accinput)
    PI = calculatePi(accinput)
    print('Pi is: {}'.format(PI))
    return terms

def calculatePi(placeIn = terms):
    if placeIn > 15:
        if input("Warning: You have chosen to calculate more than 20 digits of pi. This may take a LONG TIME and may be inacurate. Enter 'yes' if you wish to proceed. If you enter anything else, this function will revert to 10 digits.") == 'yes':
            place = placeIn
        else:
            place = 10
    else:
        place = placeIn
    print('Calculating Pi...\nPlease wait, as this may take a while.')
    PI = dec(3)
    addSub = True
    for i in range(2, 2 * (int(place) ** 6) + 1, 2):
        if addSub:
            PI += dec(4) / (dec(i) * dec(i + 1) * dec(i + 2))
        elif not addSub:
            PI -= dec(4) / (dec(i) * dec(i + 1) * dec(i + 2))
        addSub = not addSub
    return rnd(PI, -(place), mode = 'cutoff')
        
def radToDeg(radin):
    return (dec(radin) * dec(180 / pi))
    
def degToRad(degin):
    return (dec(degin) * dec(pi / 180))
        
def avg(numsIn):    #return the average of two numbers, specified as an integer or float
    num1 = dec(0)
    for i in numsIn:
        num1 += dec(i)
    return rnd(dec(num1 / dec(len(numsIn))))

def sin(anglein, dr = degrad):    #return sine of the supplied angle using the predetermined mode or the supplied mode
    if dr == 'deg':
        while anglein > 180:
            anglein -= 360
        while anglein < -180:
            anglein += 360
        angle = degToRad(anglein)
    if dr == 'rad':
        while anglein > pi:
            anglein -= (2 * pi)
        while anglein < -pi:
            anglein += (2 * pi)
        angle = anglein
    return rnd(rawsin(dec(angle)), -terms)
        
def arcsin(ratioin, dr = degrad):    #return arcsine of the supplied ratio using the predetermined mode or the supplied mode
    if ratioin > 1 or ratioin < -1:    #if the input is illegal
        return False
    attempt = dec(0)    #start at 0
    target = rnd(dec(ratioin), -terms)    #identify the target value
    #print('target is: {}'.format(target))
    for i in range(-1, int(terms) + 1):    #for each place from 10s to terms decimal place (use -i, not i)
        #print('Editing place {0}'.format(10 ** -i))    #debugging
        for j in range(10):    #for 10 steps
            #print('current attempt: {}'.format(attempt), end = ' ')
            if rnd(sin(attempt, dr), -terms) == target:
                if attempt < 0:
                    final = (attempt * dec(-1))
                else:
                    final = attempt
                #print('attempt: {0} final: {1}'.format(attempt, final))
                return final
            if rnd(sin(attempt, dr), -terms) < target:
                #add some
                attempt += (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            if rnd(sin(attempt, dr), -terms) > target:
                #subtract some
                attempt -= (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            #print('')
    if attempt < 0:
        final = (attempt * dec(-1))
    else:
        final = attempt
    #print('attempt: {0} final: {1}'.format(attempt, final))
    return (final)

def cos(anglein, dr = degrad):    #return cosine of the supplied angle
    if dr == 'deg':
        return rawsin(degToRad(90 - anglein))
    else:
        angle = anglein
        return rnd(rawsin(90 - angle), -terms)
        
def arccos(ratioin, dr = degrad):    #return arccosine of the supplied ratio
    if ratioin > 1 or ratioin < -1:
        return False
    attempt = dec(0)    #start at 0
    target = rnd(dec(ratioin), -terms)    #identify the target value
    #print('target is: {}'.format(target))
    for i in range(-1, int(terms) + 1):    #for each place from 10s to terms decimal place (use -i, not i)
        #print('Editing place {0}'.format(10 ** -i))    #debugging
        for j in range(10):    #for 10 steps
            #print('current attempt: {}'.format(attempt), end = ' ')
            if rnd(cos(attempt, dr), -terms) == target:
                if attempt < 0:
                    final = (attempt * dec(-1))
                else:
                    final = attempt
                #print('attempt: {0} final: {1}'.format(attempt, final))
                return final
            if rnd(cos(attempt, dr), -terms) < target:
                #add some
                attempt += (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            if rnd(cos(attempt, dr), -terms) > target:
                #subtract some
                attempt -= (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            #print('')
    if attempt < 0:
        final = (attempt * dec(-1))
    else:
        final = attempt
    #print('attempt: {0} final: {1}'.format(attempt, final))
    return (final)
                
def tan(anglein, dr = degrad):    #return tangent of the supplied angle
    a = sin(anglein, dr)
    b = cos(anglein, dr)
    if (not a == 0) and (not b == 0):
        return rnd((a / b), -terms)
    else:
        return False
    
def arctan(ratioin, dr = degrad):    #return arctangent of the supplied ratio
    if ratioin > 1 or ratioin < -1:
        return False
    attempt = dec(0)    #start at 0
    target = rnd(dec(ratioin), -terms)    #identify the target value
    #print('target is: {}'.format(target))
    for i in range(-1, int(terms) + 1):    #for each place from 10s to terms decimal place (use -i, not i)
        #print('Editing place {0}'.format(10 ** -i))    #debugging
        for j in range(10):    #for 10 steps
            #print('current attempt: {}'.format(attempt), end = ' ')
            if rnd(tan(attempt, dr), -terms) == target:
                if attempt < 0:
                    final = (attempt * dec(-1))
                else:
                    final = attempt
                #print('attempt: {0} final: {1}'.format(attempt, final))
                return final
            if rnd(tan(attempt, dr), -terms) < target:
                #add some
                attempt += (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            if rnd(tan(attempt, dr), -terms) > target:
                #subtract some
                attempt -= (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            #print('')
    if attempt < 0:
        final = (attempt * dec(-1))
    else:
        final = attempt
    #print('attempt: {0} final: {1}'.format(attempt, final))
    return (final)
        
def rawsin(anglein):    #return the result of sine of the supplied angle, using radians
#This is the taylor series used.
#final = x - (x^3 / 3!) + (x^5 / 5!) - (x^7 / 7!) + (x^9 / 9!) - (x^11 / 11!)...
    angle = dec(anglein)
    final = angle
    add = False
    for i in range(3, int(terms) * 3, 2):
        if add:
            final += dec(angle ** i) / fact(i)
        elif not add:
            final -= dec(angle ** i) / fact(i)
        add = not add
    return final
    
def log(valIn, baseIn = 10):
    if valIn < 1:    #if the input is illegal
        return False
    attempt = dec(0)    #start at 0
    target = rnd(dec(valIn), -terms)    #identify the target value
    #print('target is: {}'.format(target))
    for i in range(-1, int(terms) + 1):    #for each place from 10s to terms decimal place (use -i, not i)
        #print('Editing place {0}'.format(10 ** -i))    #debugging
        for j in range(10):    #for 10 steps
            print(attempt)
            #print('current attempt: {}'.format(attempt), end = ' ')
            if rnd(base ** attempt, -terms) == target:
                if attempt < 0:
                    final = (attempt * dec(-1))
                else:
                    final = attempt
                #print('attempt: {0} final: {1}'.format(attempt, final))
                return final
            if rnd(base ** attempt, -terms) < target:
                #add some
                attempt += (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            if rnd(base ** attempt, -terms) > target:
                #subtract some
                attempt -= (dec(10) ** -i)
                #print('attempt: {}'.format(attempt), end = ' ')
            #print('')
    if attempt < 0:
        final = (attempt * dec(-1))
    else:
        final = attempt
    #print('attempt: {0} final: {1}'.format(attempt, final))
    return (final)
    
def fact(intin):    #return the factorial of the given integer, return False if not given an int
    if intin == int(intin):
        intout = 1
        for i in range(1, intin + 1):
            intout *= i
        return intout
    else:
        return False
        
def rnd(numIn, decPlcIn = -terms, mode = 'fiveHigher'):    #return the given number, rounded to the given decimal place.
#use 1 to indicate 10s, 0 to indicate 1s, -2 to indicate 100ths, etc.
    num1 = dec(numIn)
    decPlc = dec(decPlcIn)
    if mode == 'fiveHigher':
        return dec(str(dec(round(num1 * (dec(10) ** -decPlc))) * (dec(10) ** decPlc)).rstrip('0'))
    elif mode == 'cutoff':
        return dec(str(dec(int(num1 * (dec(10) ** -decPlc))) * (dec(10) ** decPlc)).rstrip('0'))
    
def root(numIn, rootVal):
    num = dec(numIn)
    rt = dec(dec(1) / rootVal)
    num1 = num ** rt
    return rnd(num1, -terms)
    
def quad(aIn, bIn, cIn):    #Plugin for the quadratic formula. Provide a, b, and c.
    a = dec(aIn)
    b = dec(bIn)
    c = dec(cIn)
    try:
        posResult = (-b + root((b ** dec(2)) - (dec(4) * a * c), 2)) / (dec(2) * a)
    except:
        posResult = False
    try:
        negResult = (-b - root((b ** dec(2)) - (dec(4) * a * c), 2)) / (dec(2) * a)
    except:
        negResult = False
    return (posResult, negResult)

def abs(valIn):
    val = dec(valIn)
    if val < dec(0):
        val = val * -1
    return val