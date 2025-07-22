from __future__ import annotations
from typing import override, overload, Literal, Union
import sys

import math

## TODO: Extend (ensure all required overloads re present)

from itertools import product

components = "xyzwrgba"
swizzle_2 = list(map("".join, product(components, repeat=2)))
swizzle_3 = list(map("".join, product(components, repeat=3)))
swizzle_4 = list(map("".join, product(components, repeat=4)))

Swizzle2 = tuple(swizzle_2)
Swizzle3 = tuple(swizzle_3)
Swizzle4 = tuple(swizzle_4)

# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x : float = 0, y : float = 0):
        self.x : float = x
        self.y : float = y

    def _OnUpdate(self): ...
    
    def size(self) -> int:
        return 2

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other : Vector) -> bool:  # type: ignore
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other : Vector) -> bool:  # type: ignore
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self) -> tuple:
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other : Vector) -> Vector:
        self.x += other.x
        self.y += other.y
        
        self._OnUpdate()
        return self

    def __add__(self, other ) -> Vector:
        return self.copy().add(other)
    
        self._OnUpdate()

    # Negates the vector (makes it point in the opposite direction)
    def negate(self) -> Vector:
        
        self.multiply(-1)
        self._OnUpdate()
        return self

    def __neg__(self) -> Vector:
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other : Vector):
        return self.add(-other)

    def __sub__(self, other) -> Vector:
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k : float | int) -> Vector:
        self.x *= k
        self.y *= k
        self._OnUpdate()
        return self

    def __mul__(self, k : float | int | object) -> Vector:
        if isinstance(k, (float , int)):
            return self.copy().multiply(k)
        else:
            print(f"unknown error occured when multiplying vector {self} with {k}")
            return self

    def __rmul__(self, k : float | int) -> Vector:
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k : float) -> Vector:
        if k != 0:
            return self.multiply(1/k)
        else:
            return self.multiply(1/sys.float_info.max)

    def __truediv__(self, k : float) -> Vector:
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self) -> Vector:
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self) -> Vector:
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other : Vector) -> float:
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal : Vector) -> Vector:
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other : Vector) -> float | None:
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self) -> Vector | None:
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta : float) -> Vector | None:
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta : float) -> Vector | None:
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec : Vector)-> Vector | None:
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))


# Modified Vector class
class _Vector(Vector):

    def __init__(self, *args : float):
        self._m_vec : list [float] = []
        for arg in args:
            self._m_vec.append(arg)
        self._m_size = len(self._m_vec)

    # Returns a string representation of the vector
    def __str__(self):
        out = "("
        for value in self._m_vec:
            out += str(value)
            out += ", "
        out += ")"
        
        return out

    # Tests the equality of this vector and another
    def __eq__(self, other : _Vector) -> bool: # type: ignore
        if self._m_size != other.size(): return False
        
        equal : bool = True
        for i in range(self._m_size):
            equal = equal & (self._m_vec[i] == other[i])
        return equal

    # Tests the inequality of this vector and another
    def __ne__(self, other : _Vector): # type: ignore
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self) -> tuple:
        return tuple(self._m_vec)

    # Returns a copy of the vector
    def copy(self) -> Vector:
        return type(self)(*self._m_vec)

    @overload
    def add(self : Vec4, k : Vec4) -> Vec4: ...
    
    @overload
    def add(self : Vec3, k : Vec3) -> Vec3: ...
    
    @overload
    def add(self : Vec2, k : Vec2) -> Vec2: ...


    # Adds another vector to this vector
    def add(self, other : _Vector): # type: ignore
        if (self._m_size != other.size()):
            print(f"Attempted to add two incompatable vector types sizes: {self._m_size} {other.size()}")
        
        for i in range(self._m_size):
            self._m_vec[i] += other[i]
        
        self._OnUpdate()
        return self
    

    @overload
    def __add__(self : Vec4, other : Vec4) -> Vec4: ...
    
    @overload
    def __add__(self : Vec3, other : Vec3) -> Vec3: ...
    
    @overload
    def __add__(self : Vec2, other : Vec2) -> Vec2: ...


    def __add__(self, other) -> Vector:
        return super().__add__(other)


    @overload
    def __sub__(self : Vec4, other : Vec4) -> Vec4: ...
    
    @overload
    def __sub__(self : Vec3, other : Vec3) -> Vec3: ...
    
    @overload
    def __sub__(self : Vec2, other : Vec2) -> Vec2: ...
    
    def __sub__(self, other ) -> Vector:
        return super().__sub__(other)



    def size(self):
        return self._m_size

    @overload
    def multiply(self : Vec4, k : float) -> Vec4: ...
    
    @overload
    def multiply(self : Vec3, k : float) -> Vec3: ...
    
    @overload
    def multiply(self : Vec2, k : float) -> Vec2: ...



    
    @overload
    def __mul__(self : Vec2, k : int | float) -> Vec2: ...

    @overload
    def __mul__(self : Vec3, k : int | float) -> Vec3: ...

    @overload
    def __mul__(self : Vec4, k : int | float) -> Vec4: ...

    @overload
    def __mul__(self, k : int) -> Vector: ...

    @overload
    def __mul__(self, k : float) -> Vector: ...
    

    @overload
    def __mul__(self : Vec2, k : object) -> Vec2:
        raise NotImplemented
    @overload
    def __mul__(self : Vec3, k : object) -> Vec3:
        raise NotImplemented
    @overload
    def __mul__(self : Vec4, k : object) -> Vec4:
        raise NotImplemented

    def __mul__(self, k) -> Vector:

        if isinstance(k, (int, float)):
            return super().__mul__(k)
        else:
            return NotImplemented
    

    @overload
    def __rmul__(self : Vec2, k : int | float) -> Vec2: ...

    @overload
    def __rmul__(self : Vec3, k : int | float) -> Vec3: ...

    @overload
    def __rmul__(self : Vec4, k : int | float) -> Vec4: ...

    def __rmul__(self, k : float | int):
        return super().__rmul__(k)
    

    # Multiplies the vector by a scalar
    def multiply(self, k : float ) -> Vector:
        for i in range(self._m_size):
            self._m_vec[i] *= k
        self._OnUpdate()
        return self
    

    @overload
    def __truediv__(self : Vec2, k : int | float) -> Vec2: ...

    @overload
    def __truediv__(self : Vec3, k : int | float) -> Vec3: ...

    @overload
    def __truediv__(self : Vec4, k : int | float) -> Vec4: ...

    @overload
    def __truediv__(self, k : int) -> Vector: ...

    @overload
    def __truediv__(self, k : float) -> Vector: ...

    def __truediv__(self, k : float) -> Vector:
        if isinstance(k, (int, float)):
            return super().__mul__(1/k)
        else:
            return NotImplemented



    def __getitem__(self, index : int):
        if not ( index >= 0 and index < self._m_size ):
            print(f"list index out of range for vector of size {self._m_size}")
            assert False
            
        return self._m_vec[index]  

    def __setitem__(self, index : int, value : float):
        self._m_vec[index] = value
        self._OnUpdate()

    # Returns the dot product of this vector with another one
    def dot(self, other : _Vector): # type: ignore
        if (self._m_size != other.size()):
            print(f"Attempted to multiply two incompatable vector types sizes: {self._m_size} & {other.size()}")
            assert False
        dotP = 0
        for i in range(self._m_size):
            dotP += self._m_vec[i] * other[i]
        
        self._OnUpdate()
        return dotP
    
    def zero(self):
        for i in range(len(self._m_vec)):
            self._m_vec[i] = 0

    # Returns the length of the vector
    def length(self):
        
        return math.sqrt(self.length_squared())

    # Returns the squared length of the vector
    def length_squared(self):
        SquareSum = 0
        for value in self._m_vec:
            SquareSum += value**2
        return SquareSum

    @overload
    def normalize(self : Vec4) -> Vec4: ...
    @overload
    def normalize(self : Vec3) -> Vec3: ...
    @overload
    def normalize(self : Vec2) -> Vec2: ...

    def normalize(self) -> Vector:
        return super().normalize()


    @overload
    def get_normalized(self : Vec2) -> Vec2: ...
    
    @overload
    def get_normalized(self : Vec3) -> Vec3: ...
    
    @overload
    def get_normalized(self : Vec4) -> Vec4: ...
    
    
    def get_normalized(self):
        return super().get_normalized()

    @overload
    def divide(self : Vec4, k : float) -> Vec4: ...
    @overload
    def divide(self : Vec3, k : float) -> Vec3: ...
    @overload
    def divide(self : Vec2, k : float) -> Vector: ...

    def divide(self, k : float) -> Vector:
        return super().divide(k)

    # Returns the angle between this vector and another one
    def angle(self, other : Vector) -> None:
        print("[angle] not applicabe to this vector impl, use matrices")

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        print("[rotate_anti] not applicabe to this vector impl, use matrices")

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta : float):
        print("[rotate_rad] not applicabe to this vector impl, use matrices")

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta : float):
        print("[rotate] not applicabe to this vector impl, use matrices")

    
    # project the vector onto a given vector
    def get_proj(self, vec : Vector):
        print("[get_proj] not applicabe to this vector impl, to be implemented")

    def getIndexIfExist(self, idx) -> float:
        if abs(idx) >= self._m_size:
            return 0
        return self._m_vec[idx]

    def toVec2(self):
        return Vec2(self.getIndexIfExist(0),self.getIndexIfExist(1))
    def toVec3(self):
        return Vec3(self.getIndexIfExist(0),self.getIndexIfExist(1),self.getIndexIfExist(3))
    def toVec4(self):
        return Vec4(self.getIndexIfExist(0),self.getIndexIfExist(1),self.getIndexIfExist(2),self.getIndexIfExist(3))

class Vec2(_Vector):
    def __init__(self, x:float=0, y:float=0):
        super().__init__(x, y)
        self._OnUpdate()
    
    def perpendicular(self) -> Vec2:
        return Vec2(self.y, - self.x).normalize()
        
    def _OnUpdate(self) -> None:
        self.x : float = self._m_vec[0]
        self.y : float = self._m_vec[1]
        
        self.re : float = self._m_vec[0]
        self.im : float = self._m_vec[1]
        
    def __sizeof__(self) -> int:
        return super().__sizeof__()



    @overload
    def __getattr__(self, name: Literal["x", "y",
                                        "r", "g"]) -> float: ...

    @overload
    def __getattr__(self, name: Literal["xx", "xy",
                                        "yx", "yy",
                                        "rr", "rg",
                                        "gr", "gg"]) -> Vec2: ...

    def __getattr__(self, name):
        """Allows swizzling (e.g., vec.xy, vec.yzx, etc.)"""
        mapping = {'x': 0, 'y': 1, 'r': 0, 'i': 1, 'g' : 1}
        if all(c in mapping for c in name):
            indices = [mapping[c] for c in name]
            values  = [self._m_vec[i] for i in indices if i < len(self._m_vec)]
            if len(values) == 1:
                return values[0]
            elif len(values) == 2:
                return Vec2(*values)
            elif len(values) == 3:
                return Vec3(*values)
            elif len(values) == 4:
                return Vec4(*values)
            else:
                return Vector(*values) if len(values) > 1 else values[0]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: float) -> None:
        mapping = {'x': 0, 'y': 1, 'r': 0, 'g' : 1, 'i' : 1}
        if name in mapping:
            self._m_vec[mapping[name]] = value
        else:
            super().__setattr__(name, value)
            # raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class Vec3(_Vector):
    def __init__(self, x:float=0 , y:float=0, z:float=0):
        super().__init__(x , y , z)
        self._OnUpdate()
    
    def _OnUpdate(self) -> None:
        ...
        # self.x : float = self._m_vec[0]
        # self.y : float = self._m_vec[1]
        # self.z : float = self._m_vec[2]
        
        
        # self.r : float = self._m_vec[0]
        # self.g : float = self._m_vec[1]
        # self.b : float = self._m_vec[2]

    def toVec2(self):
        return Vec2(self.x, self.y)
    
    def get_p(self) -> tuple [float, float, float]:
        return super().get_p()



    @overload
    def __getattr__(self, name: Literal["x", "y", "z",
                                        "r", "g", "b"]) -> float: ...

    @overload
    def __getattr__(self, name: Literal["xx", "xy", "xz",
                                        "yx", "yy", "yz",
                                        "zx", "zy", "zz",

                                        "rr", "rg", "rb",
                                        "gr", "gg", "gb",
                                        "br", "bg", "bb"]) -> Vec2: ...

    @overload
    def __getattr__(self, name: Literal["xxx", "xxy", "xxz", "xyx", "xyy", "xyz", "xzx", "xzy", "xzz", 
                                        "yxx", "yxy", "yxz", "yyx", "yyy", "yyz", "yzx", "yzy", "yzz", 
                                        "zxx", "zxy", "zxz", "zyx", "zyy", "zyz", "zzx", "zzy", "zzz",

                                        "rrr", "rrg", "rrb", "rgr", "rgg", "rgb", "rbr", "rbg", "rbb",
                                        "grr", "grg", "grb", "ggr", "ggg", "ggb", "gbr", "gbg", "gbb",
                                        "brr", "brg", "brb", "bgr", "bgg", "bgb", "bbr", "bbg", "bbb"]) -> Vec3: ...

    def __getattr__(self, name):
        """Allows swizzling (e.g., vec.xy, vec.yzx, etc.)"""
        mapping = {'x': 0, 'y': 1, 'z': 2, 'r': 0, 'g': 1, 'b': 2}
        if all(c in mapping for c in name):
            indices = [mapping[c] for c in name]
            values  = [self._m_vec[i] for i in indices if i < len(self._m_vec)]
            if len(values) == 1:
                return values[0]
            elif len(values) == 2:
                return Vec2(*values)
            elif len(values) == 3:
                return Vec3(*values)
            else:
                return Vector(*values) if len(values) > 1 else values[0]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


    def __setattr__(self, name: str, value: float) -> None:
        mapping = {'x': 0, 'y': 1, 'z': 2, 'r': 0, 'g': 1, 'b': 2}
        if name in mapping:
            self._m_vec[mapping[name]] = value
        else:
            super().__setattr__(name, value)

class Vec4(_Vector):
    def __init__(self, x:float = 0, y:float = 0, z:float = 0, w:float = 0):
        super().__init__(x, y, z, w)
        self._OnUpdate()
    
    def _OnUpdate(self) -> None:
        ...
        # self.x : float = self._m_vec[0]
        # self.y : float = self._m_vec[1]
        # self.z : float = self._m_vec[2]
        # self.w : float = self._m_vec[3]


        # self.r : float = self._m_vec[0]
        # self.g : float = self._m_vec[1]
        # self.b : float = self._m_vec[2]
        # self.a : float = self._m_vec[3]

    @overload
    def __getattr__(self, name: Literal["x", "y", "z", "w",
                                        "r", "g", "b", "a"]) -> float: ...

    @overload
    def __getattr__(self, name: Literal["xx", "xy", "xz", "xw",
                                        "yx", "yy", "yz", "yw",
                                        "zx", "zy", "zz", "zw",
                                        "wx", "wy", "wz", "ww",
                                        
                                        "rr", "rg", "rb", "ra",
                                        "gr", "gg", "gb", "ga",
                                        "br", "bg", "bb", "ba",
                                        "ar", "ag", "ab", "aa"]) -> Vec2: ...

    @overload
    def __getattr__(self, name: Literal["xxx", "xxy", "xxz", "xxw", "xyx", "xyy", "xyz", "xyw", 
                                        "xzx", "xzy", "xzz", "xzw", "xwx", "xwy", "xwz", "xww", 
                                        "yxx", "yxy", "yxz", "yxw", "yyx", "yyy", "yyz", "yyw", 
                                        "yzx", "yzy", "yzz", "yzw", "ywx", "ywy", "ywz", "yww", 
                                        "zxx", "zxy", "zxz", "zxw", "zyx", "zyy", "zyz", "zyw", 
                                        "zzx", "zzy", "zzz", "zzw", "zwx", "zwy", "zwz", "zww", 
                                        "wxx", "wxy", "wxz", "wxw", "wyx", "wyy", "wyz", "wyw", 
                                        "wzx", "wzy", "wzz", "wzw", "wwx", "wwy", "wwz", "www",

                                        "rrr", "rrg", "rrb", "rra", "rgr", "rgg", "rgb", "rga", 
                                        "rbr", "rbg", "rbb", "rba", "rar", "rag", "rab", "raa", 
                                        "grr", "grg", "grb", "gra", "ggr", "ggg", "ggb", "gga", 
                                        "gbr", "gbg", "gbb", "gba", "gar", "gag", "gab", "gaa", 
                                        "brr", "brg", "brb", "bra", "bgr", "bgg", "bgb", "bga", 
                                        "bbr", "bbg", "bbb", "bba", "bar", "bag", "bab", "baa", 
                                        "arr", "arg", "arb", "ara", "agr", "agg", "agb", "aga", 
                                        "abr", "abg", "abb", "aba", "aar", "aag", "aab", "aaa"]) -> Vec3: ...

    @overload
    def __getattr__(self, name: Literal["xxxx", "xxxy", "xxxz", "xxxw", "xxyx", "xxyy", "xxyz", 
                                        "xxyw", "xxzx", "xxzy", "xxzz", "xxzw", "xxwx", "xxwy", 
                                        "xxwz", "xxww", "xyxx", "xyxy", "xyxz", "xyxw", "xyyx", 
                                        "xyyy", "xyyz", "xyyw", "xyzx", "xyzy", "xyzz", "xyzw", 
                                        "xywx", "xywy", "xywz", "xyww", "xzxx", "xzxy", "xzxz", 
                                        "xzxw", "xzyx", "xzyy", "xzyz", "xzyw", "xzzx", "xzzy", 
                                        "xzzz", "xzzw", "xzwx", "xzwy", "xzwz", "xzww", "xwxx", 
                                        "xwxy", "xwxz", "xwxw", "xwyx", "xwyy", "xwyz", "xwyw", 
                                        "xwzx", "xwzy", "xwzz", "xwzw", "xwwx", "xwwy", "xwwz", 
                                        "xwww", "yxxx", "yxxy", "yxxz", "yxxw", "yxyx", "yxyy", 
                                        "yxyz", "yxyw", "yxzx", "yxzy", "yxzz", "yxzw", "yxwx", 
                                        "yxwy", "yxwz", "yxww", "yyxx", "yyxy", "yyxz", "yyxw", 
                                        "yyyx", "yyyy", "yyyz", "yyyw", "yyzx", "yyzy", "yyzz", 
                                        "yyzw", "yywx", "yywy", "yywz", "yyww", "yzxx", "yzxy", 
                                        "yzxz", "yzxw", "yzyx", "yzyy", "yzyz", "yzyw", "yzzx", 
                                        "yzzy", "yzzz", "yzzw", "yzwx", "yzwy", "yzwz", "yzww", 
                                        "ywxx", "ywxy", "ywxz", "ywxw", "ywyx", "ywyy", "ywyz", 
                                        "ywyw", "ywzx", "ywzy", "ywzz", "ywzw", "ywwx", "ywwy", 
                                        "ywwz", "ywww", "zxxx", "zxxy", "zxxz", "zxxw", "zxyx", 
                                        "zxyy", "zxyz", "zxyw", "zxzx", "zxzy", "zxzz", "zxzw", 
                                        "zxwx", "zxwy", "zxwz", "zxww", "zyxx", "zyxy", "zyxz", 
                                        "zyxw", "zyyx", "zyyy", "zyyz", "zyyw", "zyzx", "zyzy", 
                                        "zyzz", "zyzw", "zywx", "zywy", "zywz", "zyww", "zzxx", 
                                        "zzxy", "zzxz", "zzxw", "zzyx", "zzyy", "zzyz", "zzyw", 
                                        "zzzx", "zzzy", "zzzz", "zzzw", "zzwx", "zzwy", "zzwz", 
                                        "zzww", "zwxx", "zwxy", "zwxz", "zwxw", "zwyx", "zwyy", 
                                        "zwyz", "zwyw", "zwzx", "zwzy", "zwzz", "zwzw", "zwwx", 
                                        "zwwy", "zwwz", "zwww", "wxxx", "wxxy", "wxxz", "wxxw", 
                                        "wxyx", "wxyy", "wxyz", "wxyw", "wxzx", "wxzy", "wxzz", 
                                        "wxzw", "wxwx", "wxwy", "wxwz", "wxww", "wyxx", "wyxy", 
                                        "wyxz", "wyxw", "wyyx", "wyyy", "wyyz", "wyyw", "wyzx", 
                                        "wyzy", "wyzz", "wyzw", "wywx", "wywy", "wywz", "wyww", 
                                        "wzxx", "wzxy", "wzxz", "wzxw", "wzyx", "wzyy", "wzyz", 
                                        "wzyw", "wzzx", "wzzy", "wzzz", "wzzw", "wzwx", "wzwy", 
                                        "wzwz", "wzww", "wwxx", "wwxy", "wwxz", "wwxw", "wwyx", 
                                        "wwyy", "wwyz", "wwyw", "wwzx", "wwzy", "wwzz", "wwzw", 
                                        "wwwx", "wwwy", "wwwz", "wwww",

                                        "rrrr", "rrrg", "rrrb", "rrra", "rrgr", "rrgg", "rrgb", 
                                        "rrga", "rrbr", "rrbg", "rrbb", "rrba", "rrar", "rrag", 
                                        "rrab", "rraa", "rgrr", "rgrg", "rgrb", "rgra", "rggr", 
                                        "rggg", "rggb", "rgga", "rgbr", "rgbg", "rgbb", "rgba", 
                                        "rgar", "rgag", "rgab", "rgaa", "rbrr", "rbrg", "rbrb", 
                                        "rbra", "rbgr", "rbgg", "rbgb", "rbga", "rbbr", "rbbg", 
                                        "rbbb", "rbba", "rbar", "rbag", "rbab", "rbaa", "rarr", 
                                        "rarg", "rarb", "rara", "ragr", "ragg", "ragb", "raga", 
                                        "rabr", "rabg", "rabb", "raba", "raar", "raag", "raab", 
                                        "raaa", "grrr", "grrg", "grrb", "grra", "grgr", "grgg", 
                                        "grgb", "grga", "grbr", "grbg", "grbb", "grba", "grar", 
                                        "grag", "grab", "graa", "ggrr", "ggrg", "ggrb", "ggra", 
                                        "gggr", "gggg", "gggb", "ggga", "ggbr", "ggbg", "ggbb", 
                                        "ggba", "ggar", "ggag", "ggab", "ggaa", "gbrr", "gbrg", 
                                        "gbrb", "gbra", "gbgr", "gbgg", "gbgb", "gbga", "gbbr", 
                                        "gbbg", "gbbb", "gbba", "gbar", "gbag", "gbab", "gbaa", 
                                        "garr", "garg", "garb", "gara", "gagr", "gagg", "gagb", 
                                        "gaga", "gabr", "gabg", "gabb", "gaba", "gaar", "gaag", 
                                        "gaab", "gaaa", "brrr", "brrg", "brrb", "brra", "brgr", 
                                        "brgg", "brgb", "brga", "brbr", "brbg", "brbb", "brba", 
                                        "brar", "brag", "brab", "braa", "bgrr", "bgrg", "bgrb", 
                                        "bgra", "bggr", "bggg", "bggb", "bgga", "bgbr", "bgbg", 
                                        "bgbb", "bgba", "bgar", "bgag", "bgab", "bgaa", "bbrr", 
                                        "bbrg", "bbrb", "bbra", "bbgr", "bbgg", "bbgb", "bbga", 
                                        "bbbr", "bbbg", "bbbb", "bbba", "bbar", "bbag", "bbab", 
                                        "bbaa", "barr", "barg", "barb", "bara", "bagr", "bagg", 
                                        "bagb", "baga", "babr", "babg", "babb", "baba", "baar", 
                                        "baag", "baab", "baaa", "arrr", "arrg", "arrb", "arra", 
                                        "argr", "argg", "argb", "arga", "arbr", "arbg", "arbb", 
                                        "arba", "arar", "arag", "arab", "araa", "agrr", "agrg", 
                                        "agrb", "agra", "aggr", "aggg", "aggb", "agga", "agbr", 
                                        "agbg", "agbb", "agba", "agar", "agag", "agab", "agaa", 
                                        "abrr", "abrg", "abrb", "abra", "abgr", "abgg", "abgb", 
                                        "abga", "abbr", "abbg", "abbb", "abba", "abar", "abag", 
                                        "abab", "abaa", "aarr", "aarg", "aarb", "aara", "aagr", 
                                        "aagg", "aagb", "aaga", "aabr", "aabg", "aabb", "aaba", 
                                        "aaar", "aaag", "aaab", "aaaa"]) -> Vec4: ...


    # @overload
    # def __getattr__(self, name) -> Vector:
    #     ...
                    

    def __getattr__(self, name) -> float | Vec2 | Vec3 | Vec4 | Vector:
        """Allows swizzling (e.g., vec.xy, vec.yzx, etc.)"""
        mapping = {'x': 0, 'y': 1, 'z': 2, 'w': 3, 'r': 0, 'g': 1, 'b': 2, 'a': 3}
        if all(c in mapping for c in name):
            indices = [mapping[c] for c in name]
            values  = [self._m_vec[i] for i in indices if i < len(self._m_vec)]
            if len(values) == 1:
                return values[0]
            elif len(values) == 2:
                return Vec2(*values)
            elif len(values) == 3:
                return Vec3(*values)
            elif len(values) == 4:
                return Vec4(*values)
            else:
                return Vector(*values) if len(values) > 1 else values[0]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: float) -> None:
        mapping = {'x': 0, 'y': 1, 'z': 2, 'w': 3, 'r': 0, 'g': 1, 'b': 2, 'a': 3}
        if name in mapping:
            self._m_vec[mapping[name]] = value
        else:
            super().__setattr__(name, value)

    def get_p(self) -> tuple [float, float, float, float]:
        return super().get_p()
    
    def toVec2(self):
        return Vec2(self.x, self.y)
    
    def toVec3(self):
        return Vec3(self.x, self.y, self.z)

class Color(Vec4):
    def __init__(self, x:float = 255, y:float = 255, z:float = 255, w:float = 255):
        super().__init__(x, y, z, w)
        self._OnUpdate()