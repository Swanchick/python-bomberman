from abc import ABC

from utils import Vector

class BaseWindow(ABC):
    def set_camera_pos(self, pos: Vector):
        ...
    
    def set_camera_scale(self, scale: Vector):
        ...

    def get_camera_pos(self) -> Vector:
        ...
    
    def get_camera_scale(self) -> Vector:
        ...
    
    @property
    def resolution(self) -> Vector:
        ...
