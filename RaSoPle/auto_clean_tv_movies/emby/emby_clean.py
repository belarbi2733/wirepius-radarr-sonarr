#!/usr/bin/env python3

import urllib.request as request
import json, urllib
import traceback
import hashlib
import sys
import os
from dateutil.parser import parse
from datetime import datetime,date,timedelta,timezone

# Hash password if not hashed
#if cfg.admin_password_sha1 == '':
#     cfg.admin_password_sha1=hashlib.sha1(cfg.admin_password.encode()).hexdigest()
#auth_key=''
#print('Hash:'+ cfg.admin_password_sha1)


def retjprint(rawjson):
    #return a formatted string of the python JSON object
    ezjson = json.dumps(rawjson, sort_keys=False, indent=4)
    return(ezjson)


def jprint(rawjson):
    #create a formatted string of the python JSON object
    ezjson = retjprint(rawjson)
    print(ezjson)


#emby or jellyfin?
def get_brand():
    defaultbrand='emby'
    print('0:emby\n1:jellyfin')
    brand=input('Enter number for server branding (default ' + defaultbrand + '): ')
    if (brand == ''):
        return(defaultbrand)
    elif (brand == '0'):
        return(defaultbrand)
    elif (brand == '1'):
        return('jellyfin')
    else:
        print('Invalid choice. Default to emby.')
        return(defaultbrand)


#ip address?
def get_url():
    defaulturl='http://localhost'
    url=input('Enter server ip or name (default ' + defaulturl + '): ')
    if (url == ''):
        return(defaulturl)
    else:
        if (url.find('://',3,7) >= 0):
            return(url)
        else:
           #print('No http:// or https:// entered.')
           url='http://' + url
           print('Assuming server ip or name is: ' + url)
           return(url)


#http or https port?
def get_port():
    defaultport='8096'
    valid_port=False
    while (valid_port == False):
        print('If you have not explicity changed this option, press enter for default.')
        print('Space for no port.')
        port=input('Enter port (default ' + defaultport + '): ')
        if (port == ''):
            valid_port=True
            return(defaultport)
        elif (port == ' '):
            valid_port=True
            return('')
        else:
            try:
                port_float=float(port)
                if ((port_float % 1) == 0):
                    port_int=int(port_float)
                    if ((int(port_int) >= 1) and (int(port_int) <= 65535)):
                        valid_port=True
                        return(str(port_int))
                    else:
                        print('\nInvalid port. Try again.\n')
                else:
                    print('\nInvalid port. Try again.\n')
            except:
                print('\nInvalid port. Try again.\n')


#base url?
def get_base(brand):
    defaultbase='emby'
    #print('If you are using emby press enter for default.')
    if (brand == defaultbase):
        print('Using "/' + defaultbase + '" as base url')
        return(defaultbase)
    else:
        print('If you have not explicity changed this option in jellyfin, press enter for default.')
        print('For example: http://example.com/<baseurl>')
        base=input('Enter base url (default /' + defaultbase + '): ')
        if (base == ''):
            return(defaultbase)
        else:
            if (base.find('/',0,1) == 0):
                return(base[1:len(base)])
            else:
                return(base)


#admin username?
def get_admin_username():
    return(input('Enter admin username: '))


#admin password?
def get_admin_password():
    print('Plain text password used to grab access token; hashed password stored in config file.')
    password=input('Enter admin password: ')
    return(password)


#hash admin password
def get_admin_password_sha1(password):
    #password_sha1=password #input('Enter admin password (password will be hashed in config file): ')
    password_sha1=hashlib.sha1(password.encode()).hexdigest()
    return(password_sha1)


#get user input needed to build the media_cleaner_config.py file
def generate_config():
    print('-----------------------------------------------------------')
    server_brand=get_brand()

    print('-----------------------------------------------------------')
    server=get_url()
    print('-----------------------------------------------------------')
    port=get_port()
    print('-----------------------------------------------------------')
    server_base=get_base(server_brand)
    if (len(port)):
        server_url=server + ':' + port + '/' + server_base
    else:
        server_url=server + '/' + server_base
    print('-----------------------------------------------------------')

    username=get_admin_username()
    print('-----------------------------------------------------------')
    password=get_admin_password()
    password_sha1=get_admin_password_sha1(password)
    print('-----------------------------------------------------------')

    auth_key=get_auth_key(server_url, username, password, password_sha1)
    user_key=list_users(server_url, auth_key)
    print('-----------------------------------------------------------')

    not_played_age_movie="100"
    not_played_age_episode="100"
    not_played_age_video="100"
    not_played_age_trailer="100"

    config_file=''
    config_file += "server_brand='"+ server_brand +"'\n"
    config_file += "server_url='"+ server_url +"'\n"
    config_file += "admin_username='"+ username +"'\n"
    config_file += "admin_password_sha1='"+ password_sha1 +"'\n"
    config_file += "access_token='"+ auth_key +"'\n"
    config_file += "user_key='"+ user_key +"'\n"
    config_file += "DEBUG=0\n"
    #config_file += "#----------------------------------------------------------#\n"
    #config_file += "#-1=Disable deleting for media type (movie, episode, video, trailer)#\n"
    #config_file += "# 0-365000=Delete media type once it has been watched x days ago#\n"
    #config_file += "#100=default#\n"
    config_file += "not_played_age_movie="+ not_played_age_movie +"\n"
    config_file += "not_played_age_episode="+ not_played_age_episode +"\n"
    config_file += "not_played_age_video="+ not_played_age_video +"\n"
    config_file += "not_played_age_trailer="+ not_played_age_trailer +"\n"
    #config_file += "not_played_age_audio="+ not_played_age_audio +"\n"
    #config_file += "not_played_age_season_folder="+ not_played_age_season_folder +"\n"
    #config_file += "not_played_age_tvchannel="+ not_played_age_tvchannel +"\n"
    #config_file += "not_played_age_program="+ not_played_age_program +"\n"
    #config_file += "#----------------------------------------------------------#\n"
    #config_file += "#----------------------------------------------------------#\n"
    #config_file += "#0=Disable deleting ALL media types#\n"
    #config_file += "#1=Enable deleteing ALL media types once past 'not_played_age_*' days ago#\n"
    #config_file += "#0=default#\n"
    config_file += "remove_files=0\n"
    #config_file += "#----------------------------------------------------------#\n"
    #config_file += "#----------------------------------------------------------#\n"
    #config_file += "#0=Ok to delete favorite of media type once past not_played_age_* days ago#\n"
    #config_file += "#1=Do no delete favorite of media type#\n"
    #config_file += "#(1=default)#\n"
    #config_file += "#Favoriting a series or season will treat all child episodes as if they are favorites#\n"
    config_file += "keep_favorites_movie=1\n"
    config_file += "keep_favorites_episode=1\n"
    config_file += "keep_favorites_video=1\n"
    config_file += "keep_favorites_trailer=1"
    #config_file += "keep_favorites_audio=1"
    #config_file += "keep_favorites_season_folder=1"
    #config_file += "keep_favorites_tvchannel=1"
    #config_file += "keep_favorites_program=1"
    #config_file += "\n#----------------------------------------------------------#"

    #Create config file next to the script even when cwd is not the same
    cwd = os.getcwd()
    script_dir = os.path.dirname(__file__)
    if (script_dir == ''):
        #script run from cwd
        #set script_dir to '.' (aka this directory) to prevent error when attempting to change to '' (aka a blank directory)
        script_dir='.'
    os.chdir(script_dir)
    f = open("media_cleaner_config.py", "w")
    f.write(config_file)
    f.close()
    os.chdir(cwd)

    print('\n\n-----------------------------------------------------------')
    print('Config file is not setup to delete media')
    print('To delete media set remove_files=1 in media_cleaner_config.py')
    print('-----------------------------------------------------------')
    print('Config file contents:')
    print('-----------------------------------------------------------')
    print(config_file)
    print('-----------------------------------------------------------')
    print('Config file created, try running again')
    print('-----------------------------------------------------------')


#api call to delete items
def delete_item(itemID):
    url=url=cfg.server_url +'/Items/' + itemID + '?api_key='+ cfg.access_token
    req = request.Request(url,method='DELETE')
    if bool(cfg.DEBUG):
        #DEBUG
        print(itemID)
        print(url)
        print(req)
    if bool(cfg.remove_files):
        try:
            request.urlopen(req)
        except Exception:
            print('generic exception: ' + traceback.format_exc())
    else:
        return


#api call to get admin account authentication token
def get_auth_key(server_url, username, password, password_sha1):
    #login info
    values = {'Username' : username, 'Password' : password_sha1, 'Pw' : password}
    #DATA = urllib.parse.urlencode(values)
    #DATA = DATA.encode('ascii')
    DATA = json.dumps(values)
    DATA = DATA.encode("utf-8")
    DATA = bytes(DATA)

    headers = {'X-Emby-Authorization' : 'Emby UserId="'+ username  +'", Client="media_cleaner", Device="media_cleaner", DeviceId="media_cleaner", Version="0.2", Token=""', 'Content-Type' : 'application/json'}

    req = request.Request(url=server_url + '/Users/AuthenticateByName', data=DATA, method='POST', headers=headers)

    with request.urlopen(req) as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)

            #DEBUG
            #jprint(data)
        else:
            print('An error occurred while attempting to retrieve data from the API.')

    return(data['AccessToken'])


#api call to get all user accounts
#then choose account this script will use to delete watched media
#choosen account does NOT need to have "Allow Media Deletion From" enabled
def list_users(server_url, auth_key):
    #Get all users
    with request.urlopen(server_url +'/Users?api_key=' + auth_key) as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)

            #DEBUG
            #jprint(data)
        else:
            print('An error occurred while attempting to retrieve data from the API.')

    valid_user=False
    while (valid_user == False):
        i=0
        for user in data:
            print(str(i) +':'+ user['Name'] + ' - ' + user['Id'])
            i += 1

        user_number=input('Enter number for user to track: ')
        try:
            user_number_float=float(user_number)
            if ((user_number_float % 1) == 0):
                user_number_int=int(user_number_float)
                if ((int(user_number_int) >= 0) and (int(user_number_int) < i)):
                    valid_user=True
                else:
                    print('\nInvalid number. Try again.\n')
            else:
                print('\nInvalid number. Try again.\n')
        except:
            print('\nInvalid number. Try again.\n')

    userID=data[user_number_int]['Id']
    return(userID)


#Get count of days since last watched
def get_days_since_watched(date_last_played):
    #Get current time
    date_time_now = datetime.utcnow()

    #Keep the year, month, day, hour, minute, and seconds
      #split date_last_played after seconds
    try:
        split_date_micro_tz = date_last_played.split(".")
        date_time_last_watched = datetime.strptime(date_last_played, '%Y-%m-%dT%H:%M:%S.' + split_date_micro_tz[1])
    except (ValueError):
        date_time_last_watched = 'unknown date time format'

    if bool(cfg.DEBUG):
        #DEBUG
        print(date_time_last_watched)

    if not (date_time_last_watched == 'unknown date time format'):
        date_time_delta = date_time_now - date_time_last_watched
        s_date_time_delta = str(date_time_delta)
        days_since_watched = s_date_time_delta.split(' day')[0]
        if ':' in days_since_watched:
            days_since_watched = 'Watched <1 day ago'
        elif days_since_watched == '1':
            days_since_watched = 'Watched ' + days_since_watched + ' day ago'
        else:
            days_since_watched = 'Watched ' + days_since_watched + ' days ago'
    else:
        days_since_watched='0'
    return(days_since_watched)


#get season and episode numbers
def get_season_episode(season_number, episode_number):
    season_num = str(season_number)
    season_num = season_num.zfill(2)

    episode_num = str(episode_number)
    episode_num = episode_num.zfill(2)

    season_episode = 's' + season_num + '.e' + episode_num
    return(season_episode)


#determine if series or season is set to favorite
def get_isfav_season_series(server_url, user_key, itemId, auth_key):
    #Get if season or series is marked as favorite for this item
    url=server_url + '/Users/' + user_key  + '/Items/' + itemId + '?api_key=' + auth_key

    if bool(cfg.DEBUG):
        #DEBUG
        print('-----------------------------------------------------------')
        print(url)
    with request.urlopen(url) as response:
        if response.getcode() == 200:
            source = response.read()
            isfav_data = json.loads(source)
            if bool(cfg.DEBUG):
                #DEBUG
                #jprint(isfav_data)
                pass
        else:
            print('An error occurred while attempting to retrieve data from the API.')

    return(isfav_data['UserData']['IsFavorite'])


#determine if episode is set to favorite
def get_isfav(isfav, item, server_url, user_key, auth_key):
    #Check if episode's favorite value already exists in dictionary
    if not item['Id'] in isfav['episode']:
        #Determine if this episode is marked as a favorite
        isfav['episode'][item['Id']] = item['UserData']['IsFavorite']
    #Check if season's favorite value already exists in dictionary
    if not item['SeasonId'] in isfav['season']:
        #Determine if the season is marked as a favorite
        isfav['season'][item['SeasonId']] = get_isfav_season_series(server_url, user_key, item['SeasonId'], auth_key)
    #Check if series' favorite value already exists in dictionary
    if not item['SeriesId'] in isfav['series']:
        #Determine if the series is marked as a favorite
        isfav['series'][item['SeriesId']] = get_isfav_season_series(server_url, user_key, item['SeriesId'], auth_key)
    if bool(cfg.DEBUG):
        #DEBUG
        print('-----------------------------------------------------------')
        print('Episode is favorite: ' + str(isfav['episode'][item['Id']]))
        print(' Season is favorite: ' + str(isfav['season'][item['SeasonId']]))
        print(' Series is favorite: ' + str(isfav['series'][item['SeriesId']]))

    #Check if episode, season, or series is a favorite
    if (
       (isfav['episode'][item['Id']]) or
       (isfav['season'][item['SeasonId']]) or
       (isfav['series'][item['SeriesId']]) #or
       ):
        #Either the episode, season, or series is set as a favorite
        itemIsFav=True
    else:
        #Neither the episode, season, or series is set as a favorite
        itemIsFav=False

    return(itemIsFav)


#get watched media items; track media items ready to be deleted
def get_items(server_url, user_key, auth_key):
    #Get list of all played items
    print('')
    print('-----------------------------------------------------------')
    print('Start...')
    print('Cleaning media for server at: ' + server_url)
    print('-----------------------------------------------------------')
    print('\n')
    print('-----------------------------------------------------------')
    print('Get List Of Watched Media:')
    print('-----------------------------------------------------------')

    url=server_url + '/Users/' + user_key  + '/Items?Recursive=true&IsPlayed=true&SortBy=Type,SeriesName,ParentIndexNumber,IndexNumber,Name&SortOrder=Ascending&api_key=' + auth_key

    if bool(cfg.DEBUG):
        #DEBUG
        print(url)

    with request.urlopen(url) as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)
            if bool(cfg.DEBUG):
                #DEBUG
                #jprint(data)
                pass
        else:
            print('An error occurred while attempting to retrieve data from the API.')

    #Go through all items and get ones not played in X days
    cut_off_date_movie=datetime.now(timezone.utc) - timedelta(cfg.not_played_age_movie)
    cut_off_date_episode=datetime.now(timezone.utc) - timedelta(cfg.not_played_age_episode)
    cut_off_date_video=datetime.now(timezone.utc) - timedelta(cfg.not_played_age_video)
    cut_off_date_trailer=datetime.now(timezone.utc) - timedelta(cfg.not_played_age_trailer)
    deleteItems=[]
    isfav={'episode':{},'season':{},'series':{}}

    #Determine if media item is to be deleted or kept
    for item in data['Items']:

        #find movie media items ready to delete
        if (item['Type'] == 'Movie'):
            if (
               (cfg.not_played_age_movie >= 0) and
               (item['UserData']['PlayCount'] >= 1) and
               (cut_off_date_movie > parse(item['UserData']['LastPlayedDate'])) and
               (not bool(cfg.keep_favorites_movie) or not item['UserData']['IsFavorite'])
               ):
                try:
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate']) + ' - Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ' + 'MovieID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Delete Movie: \n' + str(item))
                print(':*[DELETE] - ' + item_details)
                deleteItems.append(item)
            else:
                try:
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate']) + ' - Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ' + 'MovieID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Keep Movie: \n' + str(item))
                print(':[KEEPING] - ' + item_details)
        #find tv-episode media items ready to delete
        elif (item['Type'] == 'Episode'):
            #Get if episode, season, or series is set as favorite
            itemIsFav=get_isfav(isfav, item, server_url, user_key, auth_key)
            if (
               (cfg.not_played_age_episode >= 0) and
               (item['UserData']['PlayCount'] >= 1) and
               (cut_off_date_episode > parse(item['UserData']['LastPlayedDate'])) and
               (not bool(cfg.keep_favorites_episode) or (not itemIsFav))
               ):
                try:
                    item_details=item['Type'] + ' - ' + item['SeriesName'] + ' - ' + get_season_episode(item['ParentIndexNumber'], item['IndexNumber']) + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate']) + ' - Favorite: ' + str(itemIsFav)  + ' - ' + 'EpisodeID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Delete Episode: \n' + str(item))
                print(':*[DELETE] - ' + item_details)
                deleteItems.append(item)
            else:
                try:
                    item_details=item['Type'] + ' - ' + item['SeriesName'] + ' - ' + get_season_episode(item['ParentIndexNumber'], item['IndexNumber']) + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate']) + ' - Favorite: ' + str(itemIsFav)  + ' - ' + 'EpisodeID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Keep Episode: \n' + str(item))
                print(':[KEEPING] - ' + item_details)
        #find video media items ready to delete
        elif (item['Type'] == 'Video'):
            if (
               (item['Type'] == 'Video') and
               (cfg.not_played_age_video >= 0) and
               (item['UserData']['PlayCount'] >= 1) and
               (cut_off_date_video > parse(item['UserData']['LastPlayedDate'])) and
               (not bool(cfg.keep_favorites_video) or not item['UserData']['IsFavorite'])
               ):
                try:
                    item_details=item['Type'] + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate']) + ' -  Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ' + 'VideoID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Delete Video: \n' + str(item))
                print(':*[DELETE] - ' + item_details)
                deleteItems.append(item)
            else:
                try:
                    item_details=item['Type'] + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate'])  + ' - Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ' + 'VideoID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Keep Video: \n' + str(item))
                print(':[KEEPING] - ' + item_details)
        #find trailer media items ready to delete
        elif (item['Type'] == 'Trailer'):
            if (
               (cfg.not_played_age_trailer >= 0) and
               (item['UserData']['PlayCount'] >= 1) and
               (cut_off_date_trailer > parse(item['UserData']['LastPlayedDate'])) and
               (not bool(cfg.keep_favorites_trailer) or not item['UserData']['IsFavorite'])
               ):
                try:
                    item_details=item['Type'] + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate']) + ' -  Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ' + 'TrailerID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Delete Trailer: \n' + str(item))
                print(':*[DELETE] - ' + item_details)
                deleteItems.append(item)
            else:
                try:
                    item_details=item['Type'] + ' - ' + item['Name'] + ' - ' + get_days_since_watched(item['UserData']['LastPlayedDate'])  + ' - Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ' + 'TrailerID: ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('\nError encountered - Keep Trailer: \n' + str(item))
                print(':[KEEPING] - ' + item_details)
        #idk what these are; keep them
        else: #(item['Type'] == 'Unknown')
            try:
                item_details=item['Type'] + ' - ' + item['Name'] + ' - Favorite: ' + str(item['UserData']['IsFavorite'])  + ' - ID: ' +  item['Id']
            except (KeyError):
                item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                if bool(cfg.DEBUG):
                    #DEBUG
                    print('\nError encountered - Keep Unknown Media Type: \n' + str(item))
            print(':[KEEPING UNKNOWN MEDIA TYPE] - ' + item_details)

    if len(data['Items']) <= 0:
        print('[NO WATCHED ITEMS]')

    if bool(cfg.DEBUG):
        print('')
        print('isfav: ')
        print(isfav)
        print('')

    print('-----------------------------------------------------------')
    print('\n')
    return(deleteItems)


#list and delete items past watched threshold
def list_delete_items(deleteItems):
    #List items to be deleted
    print('-----------------------------------------------------------')
    print('Summary Of Deleted Media:')
    if not bool(cfg.remove_files):
        print('* Trial Run           *')
        print('* remove_files=0      *')
        print('* No Media Deleted    *')
        print('* Items = ' + str(len(deleteItems)))
        print('-----------------------------------------------------------')
    else:
        print('* Items Deleted = ' + str(len(deleteItems)))
        print('-----------------------------------------------------------')

    if len(deleteItems) > 0:
        for item in deleteItems:
            if item['Type'] == 'Movie':
                item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
            elif item['Type'] == 'Episode':
                try:
                    item_details=item['Type'] + ' - ' + item['SeriesName'] + ' - ' + get_season_episode(item['ParentIndexNumber'], item['IndexNumber']) + ' - ' + item['Name'] + ' - ' + item['Id']
                except (KeyError):
                    item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
                    if bool(cfg.DEBUG):
                        #DEBUG
                        print('Error encountered - Delete Episode: \n\n' + str(item))
            elif item['Type'] == 'Video':
                item_details='  ' + item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
            elif item['Type'] == 'Trailer':
                item_details=item['Type'] + ' - ' + item['Name'] + ' - ' + item['Id']
            else: # item['Type'] == 'Unknown':
                pass
            #Delete media item
            delete_item(item['Id'])
            print('[DELETED] ' + item_details)
    else:
        print('[NO ITEMS TO DELETE]')

    print('-----------------------------------------------------------')
    print('\n')
    print('-----------------------------------------------------------')
    print('Done.')
    print('-----------------------------------------------------------')
    print('')

############# START OF SCRIPT #############

try:
    #try importing the media_cleaner_config.py file
    #if media_cleaner_config.py file does not exsit go to except and create one
    import media_cleaner_config as cfg
    #try setting DEBUG variable from media_cleaner_config.py file
    #if DEBUG does not exsit go to except and completely rebuild the media_cleaner_config.py file
    test=cfg.DEBUG
    #removing DEBUG from media_cleaner_config.py file is sort of configuration reset

    #depending on what is missing from media_cleaner_config.py file; try to only ask for certain input
    if (
        not hasattr(cfg, 'server_brand') or
        not hasattr(cfg, 'server_url') or
        not hasattr(cfg, 'admin_username') or
        not hasattr(cfg, 'admin_password_sha1') or
        not hasattr(cfg, 'access_token') or
        not hasattr(cfg, 'user_key') or
        not hasattr(cfg, 'keep_favorites_movie') or
        not hasattr(cfg, 'keep_favorites_episode') or
        not hasattr(cfg, 'keep_favorites_video') or
        not hasattr(cfg, 'keep_favorites_trailer') or
        not hasattr(cfg, 'remove_files') or
        not hasattr(cfg, 'not_played_age_movie') or
        not hasattr(cfg, 'not_played_age_episode') or
        not hasattr(cfg, 'not_played_age_video') or
        not hasattr(cfg, 'not_played_age_trailer') #or
       ):
        if (
            not hasattr(cfg, 'server_brand') or
            not hasattr(cfg, 'server_url') or
            not hasattr(cfg, 'admin_username') or
            not hasattr(cfg, 'admin_password_sha1') or
            not hasattr(cfg, 'access_token') or
            not hasattr(cfg, 'user_key') #or
           ):

            if hasattr(cfg, 'server_brand'):
                delattr(cfg, 'server_brand')
            if hasattr(cfg, 'server_url'):
                delattr(cfg, 'server_url')
            if hasattr(cfg, 'admin_username'):
                delattr(cfg, 'admin_username')
            if hasattr(cfg, 'admin_password_sha1'):
                delattr(cfg, 'admin_password_sha1')
            if hasattr(cfg, 'access_token'):
                delattr(cfg, 'access_token')
            if hasattr(cfg, 'user_key'):
                delattr(cfg, 'user_key')

            print('-----------------------------------------------------------')
            server_brand=get_brand()

            print('-----------------------------------------------------------')
            server=get_url()
            print('-----------------------------------------------------------')
            port=get_port()
            print('-----------------------------------------------------------')
            server_base=get_base(server_brand)
            if (len(port)):
                server_url=server + ':' + port + '/' + server_base
            else:
                server_url=server + '/' + server_base
            print('-----------------------------------------------------------')

            username=get_admin_username()
            print('-----------------------------------------------------------')
            password=get_admin_password()
            password_sha1=get_admin_password_sha1(password)
            print('-----------------------------------------------------------')

            auth_key=get_auth_key(server_url, username, password, password_sha1)
            user_key=list_users(server_url, auth_key)
            print('-----------------------------------------------------------')

        #warn user the configuration file is not complete
        #the missing varibles are not saved and will need to be manually entered the next time the script is run
        #a new media_cleaner_config.py file will need to be completed or manually updated without duplicates
        print('\n')
        print('-----------------------------------------------------------')
        print('ATTENTION!!!')
        print('Old or incomplete config in use.')
        print('1) Delete media_cleaner_config.py and run this again to create a new config.')
        print('Or')
        print('2) Delete DEBUG from media_cleaner_config.py and run this again to create a new config.')
        print('-----------------------------------------------------------')
        print('Matching value(s) in media_cleaner_config.py ignored.')
        print('Using the below config value(s) for this run:')
        print('-----------------------------------------------------------')

        if not hasattr(cfg, 'server_brand'):
            print('server_brand=\'' + str(server_brand) + '\'')
            setattr(cfg, 'server_brand', server_brand)
        if not hasattr(cfg, 'server_url'):
            print('server_url=\'' + str(server_url) + '\'')
            setattr(cfg, 'server_url', server_url)
        if not hasattr(cfg, 'admin_username'):
            print('admin_username=\'' + str(username) + '\'')
            setattr(cfg, 'admin_username', username)
        if not hasattr(cfg, 'admin_password_sha1'):
            print('admin_password_sha1=\'' + str(password_sha1) + '\'')
            setattr(cfg, 'admin_password_sha1', password_sha1)
        if not hasattr(cfg, 'access_token'):
            print('access_token=\'' + str(auth_key) + '\'')
            setattr(cfg, 'access_token', auth_key)
        if not hasattr(cfg, 'user_key'):
            print('user_key=\'' + str(user_key) + '\'')
            setattr(cfg, 'user_key', user_key)

        if not hasattr(cfg, 'keep_favorites_movie'):
            print('keep_favorites_movie=1')
            setattr(cfg, 'keep_favorites_movie', 1)
        if not hasattr(cfg, 'keep_favorites_episode'):
            print('keep_favorites_episode=1')
            setattr(cfg, 'keep_favorites_episode', 1)
        if not hasattr(cfg, 'keep_favorites_video'):
            print('keep_favorites_video=1')
            setattr(cfg, 'keep_favorites_video', 1)
        if not hasattr(cfg, 'keep_favorites_trailer'):
            print('keep_favorites_trailer=1')
            setattr(cfg, 'keep_favorites_trailer', 1)

        if not hasattr(cfg, 'remove_files'):
            print('remove_files=0')
            setattr(cfg, 'remove_files', 0)

        if not hasattr(cfg, 'not_played_age_movie'):
            print('not_played_age_movie=100')
            setattr(cfg, 'not_played_age_movie', 100)
        if not hasattr(cfg, 'not_played_age_episode'):
            print('not_played_age_episode=100')
            setattr(cfg, 'not_played_age_episode', 100)
        if not hasattr(cfg, 'not_played_age_video'):
            print('not_played_age_video=100')
            setattr(cfg, 'not_played_age_video', 100)
        if not hasattr(cfg, 'not_played_age_trailer'):
            print('not_played_age_trailer=100')
            setattr(cfg, 'not_played_age_trailer', 100)

        print('-----------------------------------------------------------')
        print ('\n')

#the except
except (AttributeError, ModuleNotFoundError):
    #we are here because the media_cleaner_config.py file does not exist
    #this is either the first time the script is running or media_cleaner_config.py file was deleted
    #when this happens create a new media_cleaner_config.py file
    #another possible reason we are here...
    #the above attempt to set test=cfg.DEBUG failed likely because DEBUG is missing from the media_cleaner_config.py file
    #when this happens create a new media_cleaner_config.py file
    generate_config()
    #exit gracefully
    exit(0)

#find media items to be deleted
deleteItems=get_items(cfg.server_url, cfg.user_key, cfg.access_token)
#list and delete found media items
list_delete_items(deleteItems)

############# END OF SCRIPT #############
