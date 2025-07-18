# type: ignore
from Maths.Base.MathBase import *


# import ApplicationEngine.include.Maths.Vector.Vector as Vector
from Maths.Vector.Vector import *
import Maths.Matrix.Matrix as Matrix
from Maths.Matrix.Matrix import Mat2, Mat3, Mat4
import Maths.Quaternion.Quaternion as Quat

from typing import Union

## TODO : change to * imports with LNLM namespace
# class LNLMaths:

# def translate(mat : Matrix.Mat4 , vec : Matrix.Vec3) -> Matrix.Mat4:
#     retMat = mat.copy()
#     for r in range(3):
#         retMat[r , 3] = vec[r]
#     return retMat

def toMat4(q : Quat.Quat) -> Matrix.Mat4:
    x, y, z, w = q.x, q.y, q.z, q.w
    return Matrix.Mat4(
        [
            [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y, 0.0],
            [2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x, 0.0],
            [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
    )

# def toMat4(m : Matrix) -> Matrix.Mat4: ...

def inverse(matrix : Matrix.Matrix) -> Matrix.Matrix:
    """Returns the inverse of the matrix if it exists, maintaining its type."""
    if matrix.rows != matrix.cols:
        raise ValueError("Only square matrices can be inverted")
    
    size = matrix.rows
    identity = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    mat = [row[:] for row in matrix.getData()]  # Copy matrix
    
    # Perform Gaussian elimination
    for i in range(size):
        # Make diagonal element 1
        diag = mat[i][i]
        if diag == 0:
            raise ValueError("Matrix is singular and cannot be inverted")
        for j in range(size):
            mat[i][j] /= diag
            identity[i][j] /= diag
        
        # Make other elements in column 0
        for k in range(size):
            if k != i:
                factor = mat[k][i]
                for j in range(size):
                    mat[k][j] -= factor * mat[i][j]
                    identity[k][j] -= factor * identity[i][j]
    if isinstance(matrix, (Matrix.Mat2, Matrix.Mat3, Matrix.Mat4)):
        return type(matrix)()
    else:
        return Matrix.Matrix(matrix.rows, matrix.cols, sum(identity, []))
    


class LNLMAths:
    @staticmethod
    def rotate_vec2(point : Vec2, origin : Vec2, angleDeg : float) -> Vec2:
        x : float = point.x - origin.x 
        y : float = point.y - origin.y


        cos : float = math.cos(math.radians(angleDeg))        
        sin : float = math.sin(math.radians(angleDeg))        


        xp = (x * cos) - (y * sin)
        yp = (x * sin) + (y * cos)
        

        xp += origin.x
        yp += origin.y

        return Vec2(xp, yp)
    
    @staticmethod
    def reflectVec2(velocity : Vec2, axis : Vec2):
        return velocity - 2.0 * velocity.dot(axis) * axis



    @staticmethod
    def compare_f(x : float, y : float, ebsilon : float = sys.float_info.min):
        """compare two floats to a certain degree (ebsilon), used for certain physics calcs to reduce floating point err like when using floating point"""
        return abs(x - y) <= (ebsilon * max(1.0, max(abs(x), abs(y))))
    

    def compare_vec2(vecA : Vec2, vecB : Vec2, ebsilon : float = sys.float_info.min):
        """compare two vec2s to a certain degree (ebsilon), used for certain physics calcs to reduce floating point err"""
        return LNLMAths.compare_f(vecA.x, vecB.x, ebsilon) and LNLMAths.compare_f(vecA.y, vecB.y, ebsilon)