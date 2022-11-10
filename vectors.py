import math

def determinant(first, second, third):
    x = second.y * third.z - second.z * third.y
    y = first.x * third.z - first.z * third.x
    z = first.x * second.y - first.y * second.x
    return x + y + z
def linear_dependendence(other=[]):
    if len(other)>3: return False
    if len(other)==3:
        if determinant(other[0],other[1],other[2])==0: return True
        else: return False
    if len(other) == 2:
        if determinant(other[0],other[1],other[1])==0: return True
        else: return False

class vector():
    def __init__(self,x,y,z=0):
        self.x=x
        self.y=y
        self.z=z
        self.i=1
        self.j=1
        self.k=1
        self.len=math.sqrt(x**2+y**2+z**2)
    def __call__(self, *args, **kwargs):
        return str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ', len = ' + str(self.len)
    def __str__(self):
        return str(self.x)+', '+str(self.y)+', '+str(self.z)+', len = '+str(self.len)
    def __add__(self, other):
        return vector(self.x+other.x,self.y+other.y, self.z+other.z)
    def __sub__(self, other):
        return vector(self.x-other.x,self.y-other.y,self.z-other.z)
    def __mul__(self, other): #СКАЛЯРНОЕ ПРОИЗВЕДЕНИЕ!!!
        #ДЛИНА * ДЛИНА * КОСИНУС МЕЖДУ НИМИ
        #ИЛИ КООРДИНАТА1 * КООРДИНАТА1 + КООРДИНАТА2 * КООРДИНАТА2
        if type(other)==int:
            return vector(self.x*other,self.y*other,self.z*other)
        else:
            return self.x*other.x+self.y*other.y+self.z*other.z

    def collinear(self, other):
        if self.x/other.x == self.y/other.y and \
                self.x/other.x == self.z/other.z:return True
        else:return False
    def sin(self,vec1, vec2):
        pass
    def determinant(first, second, third):
        x = second.y * third.z - second.z * third.y
        y = first.x * third.z - first.z * third.x
        z = first.x * second.y - first.y * second.x
        return x+y+z
    def vector_product(self,other):#ВЕКТОРНОЕ ПРОИЗВЕДЕНИЕ!!! АКА ПЛОЩАДЬ ПАРАЛЕЛЛ!!!!!!
        # ДЛИНА * ДЛИНА * СИНУС МЕЖДУ НИМИ
        if self.collinear(other):
            return 0
        else:
            x=self.y*other.z-self.z*other.y
            y=self.x*other.z-self.z*other.x
            z=self.x*other.y-self.y*other.x
            return vector(x,y,z)
    def mixed_product(first,second,third):
        if determinant(first, second, third)==0:return 0
        else:
            x= vector.vector_product(first,second).len * third.len
            if determinant(first,second,third)>0: return x
            else: return x*-1
    def linear_dependendence(other=[]):
        if len(other)>3: return True
        if len(other)==3:
            if vector.determinant(other[0],other[1],other[2])==0: return True
            else: return False
        if len(other) == 2:
            if other[0].x/other[1].x==other[0].y/other[1].y \
                and other[0].x/other[1].x==other[0].z/other[1].z:return True
            else: return False
x=vector(3,4,5)
y=vector(4,3,5)
z=vector(6,8,10)


#короче векторное произведение = площадь паралелл = длина вектора, похрен куда направлен
#ортогональные - перпендикулярные
#
#
#