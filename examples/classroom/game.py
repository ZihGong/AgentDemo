import logging

import pygame

from AgentDemo import GameConfig, Scene, SceneConfig, ItemObject

MAIN = SceneConfig(size=(40, 30))
SCHOOL = SceneConfig(coordinate=(0, 0), size=(40, 15))
TEXT = SceneConfig(coordinate=(0, 15), size=(40, 15))


class Game:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(GameConfig.title)
        
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode(MAIN.size)
        self.surface = pygame.Surface(MAIN.size)
        
        self.school_surface = pygame.Surface(SCHOOL.size)
        self.school_scene = Scene("examples/classroom/assets/school",
                                  self.school_surface,
                                  ItemObject,
                                  logger)
        
        self.text_surface = pygame.Surface(TEXT.size)
        self.text_scene = Scene("examples/classroom/assets/text_item",
                                self.text_surface,
                                ItemObject,
                                logger)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.school_scene.draw()
            self.surface.blit(self.school_surface, SCHOOL.coordinate)
            
            self.text_scene.draw()
            self.surface.blit(self.text_surface, TEXT.coordinate)
            
            self.screen.blit(self.surface, MAIN.coordinate)
            
            pygame.display.flip()
            self.clock.tick(GameConfig.game_fps)
        
        pygame.quit()
