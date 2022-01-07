from typing import Sequence, Union, Any

import pygame
from pygame.sprite import Sprite


class CustomGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]):
        super().__init__(*sprites)

    def update(self, *args: Any, **kwargs: Any) -> bool:
        ans = False
        for sprite in self.sprites():
            ans |= sprite.update(*args, **kwargs)
        return ans
