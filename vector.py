"""
This module contains the Vector2 class, which is used to store 
a vector of two floats or ints.

Classes:
    Vector2: Stores a vector of two floats or ints.

"""

import numpy as np
import pygame as pg

from typing import Type



class Vector2:
    """
    Stores a vector of two floats.
    Can be used to store either a direction, a position, or an angle.

    Attributes:
        x (float): The x component of the vector
        y (float): The y component of the vector

    """

    def __init__(self, x : float = 0, y : float = 0) -> None:
        """
        Constructs a Vector2 object.

        Parameters:
            x (float): The x component of the vector
            y (float): The y component of the vector

        """
        self.x: float = x
        self.y: float = y
    
    def __add__(self, other : Type['Vector2']) -> Type['Vector2']:
        """
        Gets the sum of two vectors.
        """
        return Vector2(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other : Type['Vector2']) -> Type['Vector2']:
        """
        Gets the difference between two vectors.
        """
        return Vector2(self.x-other.x, self.y-other.y)
    
    def __mul__(self, other : float | int | Type['Vector2']) -> Type['Vector2']:
        """
        Gets the product of two vectors or a vector and a scalar.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)
    
    def __truediv__(self, other : Type['Vector2']) -> Type['Vector2']:
        """
        Gets the quotient of two vectors or a vector and a scalar.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)
        
    def __abs__(self) -> Type['Vector2']:
        """
        Gets the absolute value of the vector.
        """
        return Vector2(abs(self.x), abs(self.y))
    
    def __str__(self) -> str:
        """
        Returns a string that contains the attributes of the vector.
        
        """
        return "Vector2 (" + str(self.x) + ", " + str(self.y) + ")"

    def get_tuple(self) -> tuple[float]:
        """
        Returns the vector as an (x,y) tuple.
        """
        return (self.x, self.y)
    
    def rotate(self, angle : float) -> Type['Vector2']:
        """
        Returns the vector rotated around (0,0). 

        Parameters:
            angle (float): The radian measure of the angle to rotate 
                the vector around.
        """
        sin = np.sin(angle)
        cos = np.cos(angle)

        new_x = self.x * cos - self.y * sin
        new_y = self.x * sin + self.y * cos

        return Vector2(new_x, new_y)
    
    def length(self) -> float:
        """
        Returns the length of the vector as a float

        """
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def normalized(self) -> float:
        """
        Returns a vector in the same direction with the length oF 1.
        """
        length = self.length()
        if length:
            return Vector2(self.x / length, self.y / length)
        else:
            return Vector2(0,0)
    
    def angle(self) -> float:
        """
        Returns the radian measure of the vector's direction as a float.
        """
        return np.arctan2(self.y, self.x)
    
    def centered_rect(self, dimensions : Type['Vector2']) -> pg.Rect:
        """
        Constructs an axis aligned pg.Rect centered on this vector.

        Parameters:
            dimensions (Vector2): The dimensions of the rectangle
        """
        return pg.Rect((self - (dimensions / 2)).get_tuple(), 
                       dimensions.get_tuple())
    
    def from_iterable(tuple : tuple[float]) -> Type['Vector2']:
        """
        Constructs a vector from a tuple of floats.

        Parameters:
            tuple (tuple[float]): The tuple to convert to a Vector. 
                Only the first two indices will be considered.
        """
        return Vector2(tuple[0], tuple[1])
    
    def from_angle(angle : float) -> Type['Vector2']:
        """
        Constructs a normalized vector from a radian angle.

        Parameters:
            angle (float): The radian angle used to create the vector.
        """
        return Vector2(np.cos(angle), np.sin(angle))
    
    def dot(self, other : Type['Vector2']) -> float:
        """
        Returns the dot product of two vectors as a float.

        """
        return self.x * other.x + self.y * other.y
    
    def cross(self, other : Type['Vector2']) -> float:
        """
        Returns the cross product of two vectors as a float.
        """
        return self.x * other.y - self.y * other.x
    