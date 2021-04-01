import pygame
pygame.font.init()

OFFSET = 70
WIDTH, HEIGHT = 576, 640
ROWS, COLS = 10, 9
PIECE_SIZE = WIDTH // COLS             # The dim of the normal piece is 56 x 56.
SILVER = (182, 194, 204)
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)

CHECK_FONT = pygame.font.SysFont('comiscsans', 90)
PASS_GIVEUP = pygame.font.SysFont('comiscsans', 30)
PLAYER_FONT = pygame.font.SysFont('comiscsans', 30)


# loads pictures 
JANGGI_BOARD = pygame.transform.scale(pygame.image.load('Assets/board.png'), (WIDTH, HEIGHT))
BUTTON = pygame.transform.scale(pygame.image.load('Assets/button.png'), (WIDTH // 4, HEIGHT // 12))
BLUE_CANNON = pygame.transform.scale(pygame.image.load('Assets/blueCannon.png'), (PIECE_SIZE, PIECE_SIZE))
BLUE_CHARIOT = pygame.transform.scale(pygame.image.load('Assets/blueChariot.png'), (PIECE_SIZE, PIECE_SIZE))
BLUE_ELEPHANT = pygame.transform.scale(pygame.image.load('Assets/blueElephant.png'), (PIECE_SIZE, PIECE_SIZE))
BLUE_HORSE = pygame.transform.scale(pygame.image.load('Assets/blueHorse.png'), (PIECE_SIZE, PIECE_SIZE))
BLUE_SOLDIER = pygame.transform.scale(pygame.image.load('Assets/blueSoldier.png'), (PIECE_SIZE, PIECE_SIZE))
BLUE_GUARD = pygame.transform.scale(pygame.image.load('Assets/blueGuard.png'), (PIECE_SIZE, PIECE_SIZE))
BLUE_GENERAL = pygame.transform.scale(pygame.image.load('Assets/blueGeneral.png'), (PIECE_SIZE, PIECE_SIZE))
RED_CANNON = pygame.transform.scale(pygame.image.load('Assets/redCannon.png'), (PIECE_SIZE, PIECE_SIZE))
RED_CHARIOT = pygame.transform.scale(pygame.image.load('Assets/redChariot.png'), (PIECE_SIZE, PIECE_SIZE))
RED_ELEPHANT = pygame.transform.scale(pygame.image.load('Assets/redElephant.png'), (PIECE_SIZE, PIECE_SIZE))
RED_HORSE = pygame.transform.scale(pygame.image.load('Assets/redHorse.png'), (PIECE_SIZE, PIECE_SIZE))
RED_SOLDIER = pygame.transform.scale(pygame.image.load('Assets/redSoldier.png'), (PIECE_SIZE, PIECE_SIZE))
RED_GUARD = pygame.transform.scale(pygame.image.load('Assets/redGuard.png'), (PIECE_SIZE, PIECE_SIZE))
RED_GENERAL = pygame.transform.scale(pygame.image.load('Assets/redGeneral.png'), (PIECE_SIZE, PIECE_SIZE))

piece_dic = {'BLUE_CANNON': BLUE_CANNON, 'BLUE_CHARIOT': BLUE_CHARIOT, 'BLUE_ELEPHANT': BLUE_ELEPHANT, 
             'BLUE_HORSE': BLUE_HORSE, 'BLUE_SOLDIER': BLUE_SOLDIER, 'BLUE_GUARD': BLUE_GUARD, 'BLUE_GENERAL': BLUE_GENERAL, 
             'RED_CANNON': RED_CANNON, 'RED_CHARIOT': RED_CHARIOT, 'RED_ELEPHANT': RED_ELEPHANT, 'RED_HORSE' :  RED_HORSE, 
             'RED_SOLDIER' :  RED_SOLDIER, 'RED_GUARD' :  RED_GUARD, 'RED_GENERAL' :  RED_GENERAL}
