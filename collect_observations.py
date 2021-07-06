from os import path as osp
from omegaconf import DictConfig
import hydra
import pygame


from lidar.environment import BuildEnvironment
from lidar.sensor import Sensor


_module_ = osp.dirname(osp.abspath(__file__))


@hydra.main(config_path="config", config_name="config")
def main(cfg: DictConfig):

    print("Setup environment.")
    env = BuildEnvironment.from_img(
        cfg.lidar.map if osp.isabs(cfg.lidar.map) else osp.join(_module_, cfg.lidar.map)
    )
    env.gt_map = env.map.copy()
    laser = Sensor(cfg.lidar.range, env, (cfg.lidar.uncertainty.distance, cfg.lidar.uncertainty.angle))
    env.map.fill((0,0,0))
    env.infomap = env.map.copy()

    running = True
    while running:

        sensorON = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Closing the app.")
                running = False
            if pygame.mouse.get_focused():
                sensorON = True
            elif not pygame.mouse.get_focused():
                sensorON = False
            
            if sensorON:
                position = pygame.mouse.get_pos()
                laser.position = position
                sensor_data = laser.sense()
                env.data_storage(sensor_data)
                env.show_sensor_data()
            env.map.blit(env.infomap, (0,0))
            pygame.display.update()

        
        pygame.display.update()


if __name__ == "__main__":
    main()