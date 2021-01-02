# MIT License

# Copyright (c) 2020 David Rice

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Multipurpose Display Wrapper

Wrapper to support ActivityBoard and MediaPlayer functionality

Designed to run on Raspberry Pi 3 or Raspberry Pi 4

Requires PyGame 1.9.6 with Python 3.6 or higher (tested on Python 3.7.3)

TODO: Significant cleanup required

https://github.com/davidsmakerworks/multipurpose-display
"""

import json
import random

import pygame

from media_player import MediaPlayer
from activity_board import ActivityBoard
from screen import Screen


def main():
    with open('media-config.json', 'r') as f:
        media_config = json.load(f)

    with open('activity-config.json', 'r') as f:
        activity_config = json.load(f)

    # Small buffer size to prevent delays when playing sounds
    pygame.mixer.init(buffer=512)
    pygame.init()

    random.seed()

    # Need to hide mouse pointer here since the other classes
    # might be used to render on a surface instead of a display
    pygame.mouse.set_visible(False)

    screen = Screen(
        width=activity_config['display']['width'],
        height=activity_config['display']['height'],
        bg_color=pygame.Color(activity_config['board']['bg_color']),
        fullscreen=activity_config['display']['fullscreen'])

    screen_surface = screen.surface
    play_again = True

    while True:
        while play_again:
            player = MediaPlayer(
                surface=screen_surface,
                config=media_config,
                surface_is_display=True)

            play_again = player.run()

        play_again = True

        while play_again:
            board = ActivityBoard(
                surface=screen_surface,
                config=activity_config,
                start_hidden=True,
                surface_is_display=True)

            play_again = board.run()

        play_again = True


if __name__ == '__main__':
    main()