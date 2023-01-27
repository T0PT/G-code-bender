import math
import numpy as np

def normal( func=math.sin, accuracy=0.01, point=1, multiplier=0.01): # suposed to output angle from horizontal to normal (in radians)
    #multiplier - squizes function, needs to be  ???
    # slope - tangens of angle of tangent line to horizon
    if (func(point+0.5*accuracy)-func(point-0.5*accuracy))==0: return 0
    slope=accuracy/(func(point+0.5*accuracy)*multiplier-func(point-0.5*accuracy)*multiplier )
    if slope > 0: slope=-1*slope
    slope=math.atan(slope)
    return slope+1.5

class gcode():

    def __init__(self, file=''):
        self.path=file
    
    def bend(self, func=math.sin, min_func=0.5*math.pi, max_func=2.5*math.pi, plane='X', plane2='Z', offset=10, func_mul=20):
        started=False
        layerno=0
        allayers=0
        lastplanes={'X':0, 'Y':0, 'Z':0, 'F':0}
        with open(self.path, 'r') as inpt:
            for currline in inpt:
                if 'LAYER:' in currline: allayers = int(currline[7:])  
        values=[func(i)*func_mul for i in np.arange(min_func, max_func, (max_func-min_func)/allayers)]#*(1-1/allayers)]   
        #print(values)   
        #range(min,max, float(max-min)/float(worklayermax-worklayermin))
        #values = [x for x in range(500)]
        with open(self.path, 'r') as inpt, open('documnt.txt', 'w+') as output:
            count=1
            for currline in inpt:
                out=''
                if 'LAYER:' in currline: layerno = int(currline[7:])
                if ';end of start g-code' in currline or ';start of end g-code' in currline: started= not started
                if started == False:
                    output.write(currline)
                    count+=1
                else:
                    if 'G0' not in currline and 'G1' not in currline: 
                        output.write(currline)
                        count+=1
                    else:
                        out+=currline[:2]+' '
                        vals=lastplanes                      
                        vals.update({currline[3]:currline[4:currline.find(' ',3)]})
                        last=currline.find(' ',3)                        
                        while True:   
                            if last==-1: break                          
                            vals.update({currline[last+1]:currline[last+2: currline.find(' ', last+1)]})                            
                            last=currline.find(' ', last+1)
                        if count >=3925 and count<=3935: print(str(count)+ '   '+str(lastplanes)+'...'+str(vals))
                        lastplanes.update(vals)
                        if count >=3925 and count<=3935: print(str(count)+ '   '+str(lastplanes)+'///'+str(vals))
                        norm=normal(func=func,point=layerno/allayers*((max_func-min_func)+min_func), multiplier=1/allayers*1*func_mul)               
                        # let's bend :)                        
                        #vals.update({plane2: (math.sin(norm)*(float(vals[plane])-offset))+float(vals[plane2])})#                       
                        vals.update({plane: values[layerno-1]+float(vals[plane])})#math.cos(norm)*
                        #foooh
                        if count >=3925 and count<=3935: print(str(count)+ '   '+str(lastplanes)+'   '+str(vals))
                        for key,value in vals.items():
                            if key in currline or key in [plane, plane2]:
                                out+=key+str(round(float(value),3))+' '
                        output.write(out+'\n')
                        count+=1
                           
        print('DONE')
        with open('documnt.txt', 'r') as inpt, open(self.path[:-6]+'_bent.gcode', 'w+') as output:
            for line in inpt:
                output.write(line)
        print('DUMPED')    

cod=gcode('FBG5_xyzCalibration_cube.gcode')
cod.bend(offset=10)


