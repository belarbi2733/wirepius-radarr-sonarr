#!/usr/bin/env python
# -*- coding: utf-8 -*-
# To get token you need to execute this script : python plex-gettoken.py

import os
from datetime import datetime
from plexapi.server import PlexServer

datestr = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print('%s Starting plex-autotag script..' % datestr())
    plex = PlexServer('http://10.2.0.15:32400', 'TOKEN')
    for section in plex.library.sections():
        if section.type in ('show',):
            for show in section.all():
                if len(show.collections) == 0:
                    print('Adding keep1 to %s' % show.title)
                    show.addCollection(['keep1'])