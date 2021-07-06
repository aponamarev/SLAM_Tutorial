from os import path as osp
from omegaconf import DictConfig
import hydra
import pygame

from lidar.environment import BuildEnvironment


_module_ = osp.dirname(osp.abspath(__file__))


@hydra.main(config_path="config", config_name="config")
def main(cfg: DictConfig):

    print("Setup environment.")
    env = BuildEnvironment.from_img(
        cfg.lidar.map if osp.isabs(cfg.lidar.map) else osp.join(_module_, cfg.lidar.map)
    )

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Closing the app.")
                running = False
        
        pygame.display.update()


if __name__ == "__main__":
    main()