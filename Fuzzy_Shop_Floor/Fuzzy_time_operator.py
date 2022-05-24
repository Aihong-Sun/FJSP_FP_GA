'''
operation of fuzzy time
Contain function: add(X,Y);Measure(X,Y);
'''

def add(X,Y):
    return [X[_]+Y[_] for _ in range(3)]

def TFN_value(X):
    return (X[0] + 2 * X[1] + X[2]) / 4

def Measure(X,Y):
    F_X=TFN_value(X)
    F_Y=TFN_value(Y)
    if F_X!=F_Y:
        if F_X>F_Y:return True
        else:return False
    else:
        if X[1]!=Y[1]:
            if X[1]>Y[1]:return True
            else:return False
        else:
            if X[2]-X[0]>Y[2]-Y[0]:return True
            else:return False

