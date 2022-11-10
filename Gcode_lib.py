import numpy as np
import math
#import vectors

def normal( func=math.sin, accuracy=0.01, point=1): # suposed to output angle from horizontal to normal (in radians)
    slope=(func(point+0.5*accuracy)-func(point-0.5*accuracy))/accuracy
    if slope==0: return 0    
    slope=math.atan(slope)
    return slope-0.5

class gcode():

    def line(self, lastpos=[0, 0, 0,], nextpos=[0,0,0,0,0]): #nextpos[0]-x, nextpos[1]-y, nextpos[2]-z, nextpos[3]-e, nextpos[4]-f
        cod = ''
        if nextpos[3] == 0:
            cod += 'G0'
        else:
            cod += 'G1'
        if nextpos[0] != 0:
            cod += ' X' + str(lastpos[0] + nextpos[0])
            lastpos[0] += nextpos[0]
        if nextpos[1] != 0:
            cod += ' Y' + str(lastpos[1] + nextpos[1])
            lastpos[1] += nextpos[1]
        if nextpos[2] != 0:
            cod += ' Z' + str(lastpos[2] + nextpos[2])
            lastpos[2] += nextpos[2]
        if nextpos[3] != 0:
            cod += ' E' + str(lastpos[3] + nextpos[3])
            lastpos[3] += nextpos[4]
        if nextpos[4] != 0: cod += ' F' + str(nextpos[4])
        return cod
    def __init__(self, location=''):
        self.location=location
        self.loaded=False

    def move(self, func=math.sin, min_func=0.5*math.pi, max_func=2*math.pi, min_onmodel=0, max_onmodel=1, plane='X', weight=20):   #func-funcion, min-minimum argument value of the function, max_func-maximum value, min-FUNC_onmodel-where to start bending(from 0 to 1),
        # max_onmodel-where to end, plane-says in which plane to bend(letter need to be capital)
        if min_onmodel>1 or min_onmodel<0 or max_onmodel>1 or max_onmodel<0:
            print('Check arguments, some of them are more or less than possible')
            return 0
        started=False
        global layerno
        layerno=-1
        global allayers
        global worklayermin
        global worklayermax
        global num
        num=0
        with open(self.location, 'r') as inpt:
            for currline in inpt:
                if 'LAYER:' in currline: allayers = int(currline[7:])
        worklayermin = int(allayers * min([min_onmodel,max_onmodel]))
        worklayermax = int(allayers * max([min_onmodel,max_onmodel]))
        values=[func(x) for x in  np.arange(min_func,max_func, float(max_func-min_func)/float(worklayermax-worklayermin)* (1-(1/(worklayermax-worklayermin))))] #range(min,max, float(max-min)/float(worklayermax-worklayermin))
        #values = [x for x in range(500)]
        with open(self.location, 'r') as inpt, open('documnt.txt', 'w+') as output:
            for currline in inpt:
                # print(currline)
                if 'LAYER:' in currline: layerno = int(currline[7:])
                if ';end of start g-code' in currline or ';start of end g-code' in currline: started= not started
                # print(layerno)
                if started == False:
                    output.write(currline)
                else:
                    if 'G1' in currline and plane in currline or 'G0' in currline and plane in currline:
                        nom = currline.find(plane)+1
                        nextnom = currline.find(" ", nom)
                        out = currline[:nom-1]
                        #print(layerno)
                        #print(worklayermin)
                        #print(worklayermax)
                        #print(len(values))
                        #if len(values)<= (worklayermax-worklayermin):print('vse ploxo  ' + str(len(values)-(worklayermax-worklayermin)))
                        if layerno<=worklayermax and layerno>=worklayermin:
                            num = round(float(currline[nom:nextnom]) + (values[layerno-worklayermin] * weight), 3)
                        elif layerno>worklayermax:
                            num = round(float(currline[nom:nextnom]) + (values[worklayermax-worklayermin] * weight), 3)
                        else:
                            num = float(currline[nom:nextnom])
                        out += plane + str(num) + currline[nextnom:]
                        output.write(out)
                        #print('ooo '+out)
                    else:
                        output.write(currline)
        print('DONE')

    def bend(self, funcion=math.sin, min_func=0, max_func=2*math.pi, min_onmodel=0, max_onmodel=1, plane='X', plane2='Z', plane3 = True, weight=20):
        #func-funcion, min-minimum argument value of the function, max_func-maximum value, min-FUNC_onmodel-where to start bending(from 0 to 1),
        # max_onmodel-where to end, plane-says in which plane to move(letter, need to be capital, 'X' or 'Y'), plane2 - says in which plane needs
        # to bend lines, plane3 - says to stretch thickness of lines or no. ///plane-X or Y, plane2-Z, plane3-E(True)
        if min_onmodel>1 or min_onmodel<0 or max_onmodel>1 or max_onmodel<0:
            print('Check arguments, some of them are more or less than possible')
            return 0
        if plane not in ['X','Y','Z','E'] or plane2 not in ['X','Y','Z','E']:
            print('Check arguments, I think you did something wrong with planes')
            return 0
        started=False
        global layerno
        layerno=-1
        global allayers
        global worklayermin
        global worklayermax
        global nom
        global nom2
        global num
        norm=1
        num=0
        with open(self.location, 'r') as inpt:
            for currline in inpt:
                if 'LAYER:' in currline: allayers = int(currline[7:])
        worklayermin = int(allayers * min([min_onmodel,max_onmodel]))
        worklayermax = int(allayers * max([min_onmodel,max_onmodel]))
        values=[funcion(x) for x in  np.arange(min_func,max_func, float(max_func-min_func)/float(worklayermax-worklayermin)* (1-(1/(worklayermax-worklayermin))))] #range(min,max, float(max-min)/float(worklayermax-worklayermin))
        #values = [x for x in range(500)]
        with open(self.location, 'r') as inpt, open('documnt.txt', 'w+') as output:
            for currline in inpt:
                # print(currline)
                if 'LAYER:' in currline: layerno = int(currline[7:])
                if ';end of start g-code' in currline or ';start of end g-code' in currline: started= not started
                # print(layerno)
                if started == False:
                    output.write(currline)
                else:
                    if 'G1' in currline and plane in currline or 'G0' in currline and plane in currline:
                        out = currline[:2]+' '
                        xpos=currline.find('X')+1
                        ypos = currline.find('Y')+1
                        zpos = currline.find('Z')+1
                        epos = currline.find('E')+1
                        fpos = currline.find('F')+1
                        xval=currline[xpos:currline.find(" ", xpos)]
                        yval = currline[ypos:currline.find(" ", ypos)]
                        zval = currline[zpos:currline.find(" ", zpos)]
                        eval = currline[epos:currline.find(" ", epos)]
                        fval = currline[fpos:currline.find(" ", fpos)]
                        if plane=='X':nom=float(xval)
                        elif plane=='Y': nom=float(yval)
                        elif plane == 'Z': nom = float(zval)
                        elif plane == 'E':nom = float(eval) 
                        #nom - plane value, nom2 - plane2 value, num - modified nom, num2 - modified nom2
                        if plane2=='X' and xpos!=0 :nom2=float(xval)
                        elif plane2=='Y' and ypos!=0 : nom2=float(yval)
                        elif plane2 == 'Z' and zpos!=0 : nom2 = float(zval)
                        elif plane2 == 'E' and epos!=0 :nom2 = float(eval)
                        norm = normal(func=funcion, point=(max_func - min_func) * layerno / allayers)#to optimize
                        # print(layerno)
                        #print(worklayermin)
                        #print(worklayermax)
                        #print(len(values))
                        #if len(values)<= (worklayermax-worklayermin):print('vse ploxo  ' + str(len(values)-(worklayermax-worklayermin)))
                        if layerno<=worklayermax and layerno>=worklayermin:
                            num2 = round(nom2+ nom*math.sin(norm), 3)
                        elif layerno>worklayermax:
                            num2 = round(nom2+ nom*math.sin(norm), 3)
                        else:
                            num2 = nom2

                        if layerno<=worklayermax and layerno>=worklayermin:                            
                            num = round(nom + (values[layerno-worklayermin]  * weight)- nom*math.sin(norm), 3)
                        elif layerno > worklayermax:
                            num = round(nom + (values[worklayermax-worklayermin] * weight)- nom*math.sin(norm), 3)
                        else:
                            num = nom
                        
                        out+=plane+str(num)+' ' + plane2 + str(num2) + ' '
                        if xpos!=0 and 'X' not in out: out+= 'X' + str(xval)+' '
                        if ypos != 0 and 'Y' not in out: out += 'Y' + str(yval)+' '
                        if zpos != 0 and 'Z' not in out: out += 'Z' + str(zval)+' '
                        if epos != 0 and 'E' not in out: out += 'E' + str(eval)+' '
                        if fpos != 0 and 'F' not in out: out += 'F' + str(fval) + ' '
                        out+='\n'
                        output.write(out)
                        #print('done')
                        #print('ooo '+out)
                    else:
                        output.write(currline)
                #print(norm)
        print('DONE')

    def dump(self):
        with open('documnt.txt', 'r') as inpt, open(self.location[:-6]+'_bent.gcode','w+') as output:
            for x in inpt:
                output.write(x)
        self.loaded=False
        print('DUMPED')
        
def straight(x): return x

cod=gcode('FBG5_xyzCalibration_cube.gcode')
cod.bend(weight=10,max_func=2*math.pi, funcion=math.sin,min_func=0.4*math.pi)
#scod.move()
cod.dump()
#cod=gcode('FBG5_pikachu_1gen_flowalistik_bent.gcode')
#cod.move(plane='Y', weight=20, min_onmodel=1, max_onmodel=0,max_func=2*math.pi)
#cod.dump()

