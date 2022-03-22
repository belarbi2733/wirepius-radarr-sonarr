#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plex-AutoDelete is a useful to delete all but the last X episodes of a show.
This comes in handy when you have a show you keep downloaded, but do not
religiously keep every single episode that is downloaded.

Usage:
Intended usage is to add one of the tags keep0, keep1, keep5, keep10, keep15, keepSeason, to
any show you want to have this behaviour. Then simply add this script to run on
a schedule and you should be all set.

Example Crontab:
@daily /home/atodd/plex-autodelete.py >> /home/atodd/plex-autodelete.log 2>&1
"""
# To get token you need to execute this script : python plex-gettoken.py

import os
from datetime import datetime
from plexapi.server import PlexServer

TAGS = {'keep0':0, 'keep1':1, 'keep3':3, 'keep5':5, 'keep10':10, 'keep15':15, 'keepSeason':'season'}
datestr = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def delete_episode(episode):
    for media in episode.media:
        for mediapart in media.parts:
            try:
                filepath = mediapart.file
                print('%s Deleting %s.' % (datestr(), filepath))
                os.unlink(filepath)
                dirname = os.path.dirname(filepath)
                if not os.listdir(dirname):
                    print('%s Removing empty directory %s.' % (datestr(), dirname))
                    os.rmdir(dirname)
            except Exception as err:
                print('%s Error deleting %s; %s' % (datestr(), filepath, err))

def keep_episodes(show, keep):
    """ Delete all but last count episodes in show. """
    deleted = 0
    episodes = show.episodes()
    if len(episodes) <= keep:
        return deleted
    sort = lambda x:x.seasonEpisode
    items = sorted(episodes, key=sort, reverse=True)
    for episode in items[keep:]:
        #delete_episode(episode)
        #deleted += 1
        if show.title == 'Charmed':
            print(episode.isWatched)
        if episode.isWatched:
            print(episode)
            delete_episode(episode)
            deleted += 1
    return deleted


def keep_season(show, keep):
    """ Keep only the latest season. """
    deleted = 0
    print('%s Cleaning %s to latest season.' % (datestr(), show.title))
    seasons = list(filter(lambda season: season.isWatched, show.seasons()))
    for season in seasons:
        for episode in season.episodes():
            episode.delete()
            deleted += 1
    return deleted


def auto_delete():
    print('%s Starting plex-autodelete script..' % datestr())
    plex = PlexServer('http://10.2.0.15:32400', 'TOKEN')
    for section in plex.library.sections():
        if section.type in ('show',):
            deleted = 0
            for tag, keep in TAGS.items():
                func = keep_season if keep == 'season' else keep_episodes
                for show in section.search(collection=tag):
                    deleted += func(show, keep)


if __name__ == '__main__':
    auto_delete()