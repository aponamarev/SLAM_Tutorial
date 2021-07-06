import pygame
import math
import numpy as np
from .environment import BuildEnvironment
from tools import reporting as rprt


class Sensor(object):
    """Lidar sensor - simulator.

    """

    range: float
    map: BuildEnvironment
    cov: np.ndarray
    sense_obstacles: list
    position: tuple
    dtype: type
    obstacle_color: tuple

    def __init__(self, range: float, map: BuildEnvironment, uncertainty: tuple, speed: float=4.0, dtype=np.float32) -> None:
        """

        Args:
            range (float): sensor range
            map (BuildEnvironment): environment map
            uncertainty (tuple): x,y uncertainty
            speed (float, optional): [description]. Defaults to 4.0.
            dtype ([type], optional): data type. Defaults to np.float32.
        """

        # pre-conditions
        rprt.is_instance(range, (float, int), prefix=__name__)
        rprt.is_instance(map, BuildEnvironment, prefix=__name__)
        rprt.is_instance(speed, (float, int), prefix=__name__)
        rprt.is_greater(speed, 0, prefix=__name__)

        self.range = range
        self.cov = np.diag(np.power(np.array([uncertainty[0], uncertainty[1]], dtype=dtype), 2))
        self.position = (0.0, 0.0)
        self.map = map
        self.W, self.H = pygame.display.get_surface().get_size()
        self.sense_obstacles = list()
        self.dtype = dtype
        self.obstacle_color = (0,0,0)
    
    def uncertainty_add(self, distance: float, angle: float, cov: np.ndarray) -> tuple:
        """Apply multivariate gaussian noise to distance and angle measurements.

        Args:
            distance (float): distance
            angle (float): angle
            cov (np.ndarray): distance and angle covariance

        Returns:
            tuple: distance+, angle+
        """
        mean = np.array([distance, angle], self.dtype)
        distance, angle = np.random.multivariate_normal(mean=mean, cov=cov)
        distance = max(distance, 0)
        angle = max(angle, 0)
        return [distance, angle]
    
    def distance(self, obstacle_positions):

        px, py = [(obstacle_positions[i] - self.position[i])**2 for i in (0, 1)]

        return math.sqrt(px+py)

    def sense(self, angle_samples: float=60, linear_samples: float=100) -> list:

        data = list()

        x0, y0 = self.position[:2]
        range = self.range

        for angle in np.linspace(0, math.pi*2, angle_samples, False):

            xn, yn = (x0 + range*math.cos(angle), y0 + range*math.sin(angle))

            for x1, y1 in zip(np.linspace(x0, xn, linear_samples, False), np.linspace(yn, y0, linear_samples, False)):

                if (0<x1<self.W) and (0<y1<self.H):
                    c = self.map.gt_map.get_at((int(x1), int(y1)))
                    if (c[0]==self.obstacle_color[0]) and ((c[1]==self.obstacle_color[1])) and ((c[2]==self.obstacle_color[2])):
                        distance = self.distance((x1, y1))
                        output = self.uncertainty_add(distance, angle, self.cov)
                        output.append(self.position)
                        data.append(output)
                        break
            
        return data


