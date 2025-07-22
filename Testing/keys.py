import pygame

# Initialize Pygame to make sure key constants are loaded
pygame.init()

# Get all attributes from the pygame module that start with "K_"
key_map: dict[int, str] = {
    getattr(pygame, name) : "PLT_KeyData()" 
    for name in dir(pygame)
    if name.startswith("K_") and isinstance(getattr(pygame, name), int)
}

# Optional: pretty-print the dictionary
import pprint
pprint.pprint(key_map)
