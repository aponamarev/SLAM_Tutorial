import math
import pygame

from tools import reporting


class Colors(object):

    black: (tuple) = (0,0,0)
    grey: (tuple) = (70,70,70)
    blue: (tuple) = (0,0,255)
    green: (tuple) = (0,255,0)
    red: (tuple) = (255,0,0)
    white: (tuple) = (255,255,255)


class BuildEnvironment(object):

    point_cloud: list

    @classmethod
    def from_img(cls, path: str):

        return BuildEnvironment(path=path, map_dim=(-1, -1)) 
    
    def __init__(self, path: str, map_dim: tuple=(-1, -1)) -> None:
        """

        Args:
            path (str): path to the map file
            map_dim (tuple): hight and width of the map. Defaults to (-1, -1) - use file dimentions.
        """
        # preconditions
        reporting.assert_is_instance(path, str, prefix=__name__)
        reporting.assert_is_not_empty(path, prefix=__name__) 
        reporting.assert_path_exists(path=path, prefix=__name__)

        pygame.init()
        self.point_cloud = []
        self.gt_map = pygame.image.load(path)
        self.mapw, self.maph = self.gt_map.get_width(), self.gt_map.get_height()
        self.widow_title = "RRT path planning"
        pygame.display.set_caption(self.widow_title)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.gt_map, (0,0))

        

