from __future__ import unicode_literals

import datetime as dt

from mopidy.frontends.mpd.exceptions import MpdNoExistError, MpdNotImplemented
from mopidy.frontends.mpd.protocol import handle_request
from mopidy.frontends.mpd.translator import playlist_to_mpd_format


@handle_request(r'^listplaylist (?P<name>\w+)$')
@handle_request(r'^listplaylist "(?P<name>[^"]+)"$')
def listplaylist(context, name):
    """
    *musicpd.org, stored playlists section:*

        ``listplaylist {NAME}``

        Lists the files in the playlist ``NAME.m3u``.

    Output format::

        file: relative/path/to/file1.flac
        file: relative/path/to/file2.ogg
        file: relative/path/to/file3.mp3
    """
    playlists = context.core.playlists.filter(name=name).get()
    if not playlists:
        raise MpdNoExistError('No such playlist', command='listplaylist')
    return ['file: %s' % t.uri for t in playlists[0].tracks]


@handle_request(r'^listplaylistinfo (?P<name>\w+)$')
@handle_request(r'^listplaylistinfo "(?P<name>[^"]+)"$')
def listplaylistinfo(context, name):
    """
    *musicpd.org, stored playlists section:*

        ``listplaylistinfo {NAME}``

        Lists songs in the playlist ``NAME.m3u``.

    Output format:

        Standard track listing, with fields: file, Time, Title, Date,
        Album, Artist, Track
    """
    playlists = context.core.playlists.filter(name=name).get()
    if not playlists:
        raise MpdNoExistError('No such playlist', command='listplaylistinfo')
    return playlist_to_mpd_format(playlists[0])


@handle_request(r'^listplaylists$')
def listplaylists(context):
    """
    *musicpd.org, stored playlists section:*

        ``listplaylists``

        Prints a list of the playlist directory.

        After each playlist name the server sends its last modification
        time as attribute ``Last-Modified`` in ISO 8601 format. To avoid
        problems due to clock differences between clients and the server,
        clients should not compare this value with their local clock.

    Output format::

        playlist: a
        Last-Modified: 2010-02-06T02:10:25Z
        playlist: b
        Last-Modified: 2010-02-06T02:11:08Z

    *Clarifications:*

    - ncmpcpp 0.5.10 segfaults if we return 'playlist: ' on a line, so we must
      ignore playlists without names, which isn't very useful anyway.
    """
    result = []
    for playlist in context.core.playlists.playlists.get():
        if not playlist.name:
            continue
        result.append(('playlist', playlist.name))
        last_modified = (
            playlist.last_modified or dt.datetime.now()).isoformat()
        # Remove microseconds
        last_modified = last_modified.split('.')[0]
        # Add time zone information
        # TODO Convert to UTC before adding Z
        last_modified = last_modified + 'Z'
        result.append(('Last-Modified', last_modified))
    return result


@handle_request(r'^load "(?P<name>[^"]+)"$')
def load(context, name):
    """
    *musicpd.org, stored playlists section:*

        ``load {NAME}``

        Loads the playlist ``NAME.m3u`` from the playlist directory.

    *Clarifications:*

    - ``load`` appends the given playlist to the current playlist.
    """
    playlists = context.core.playlists.filter(name=name).get()
    if not playlists:
        raise MpdNoExistError('No such playlist', command='load')
    context.core.tracklist.add(playlists[0].tracks)


@handle_request(r'^playlistadd "(?P<name>[^"]+)" "(?P<uri>[^"]+)"$')
def playlistadd(context, name, uri):
    """
    *musicpd.org, stored playlists section:*

        ``playlistadd {NAME} {URI}``

        Adds ``URI`` to the playlist ``NAME.m3u``.

        ``NAME.m3u`` will be created if it does not exist.
    """
    raise MpdNotImplemented  # TODO


@handle_request(r'^playlistclear "(?P<name>[^"]+)"$')
def playlistclear(context, name):
    """
    *musicpd.org, stored playlists section:*

        ``playlistclear {NAME}``

        Clears the playlist ``NAME.m3u``.
    """
    raise MpdNotImplemented  # TODO


@handle_request(r'^playlistdelete "(?P<name>[^"]+)" "(?P<songpos>\d+)"$')
def playlistdelete(context, name, songpos):
    """
    *musicpd.org, stored playlists section:*

        ``playlistdelete {NAME} {SONGPOS}``

        Deletes ``SONGPOS`` from the playlist ``NAME.m3u``.
    """
    raise MpdNotImplemented  # TODO


@handle_request(
    r'^playlistmove "(?P<name>[^"]+)" '
    r'"(?P<from_pos>\d+)" "(?P<to_pos>\d+)"$')
def playlistmove(context, name, from_pos, to_pos):
    """
    *musicpd.org, stored playlists section:*

        ``playlistmove {NAME} {SONGID} {SONGPOS}``

        Moves ``SONGID`` in the playlist ``NAME.m3u`` to the position
        ``SONGPOS``.

    *Clarifications:*

    - The second argument is not a ``SONGID`` as used elsewhere in the protocol
      documentation, but just the ``SONGPOS`` to move *from*, i.e.
      ``playlistmove {NAME} {FROM_SONGPOS} {TO_SONGPOS}``.
    """
    raise MpdNotImplemented  # TODO


@handle_request(r'^rename "(?P<old_name>[^"]+)" "(?P<new_name>[^"]+)"$')
def rename(context, old_name, new_name):
    """
    *musicpd.org, stored playlists section:*

        ``rename {NAME} {NEW_NAME}``

        Renames the playlist ``NAME.m3u`` to ``NEW_NAME.m3u``.
    """
    raise MpdNotImplemented  # TODO


@handle_request(r'^rm "(?P<name>[^"]+)"$')
def rm(context, name):
    """
    *musicpd.org, stored playlists section:*

        ``rm {NAME}``

        Removes the playlist ``NAME.m3u`` from the playlist directory.
    """
    raise MpdNotImplemented  # TODO


@handle_request(r'^save "(?P<name>[^"]+)"$')
def save(context, name):
    """
    *musicpd.org, stored playlists section:*

        ``save {NAME}``

        Saves the current playlist to ``NAME.m3u`` in the playlist
        directory.
    """
    raise MpdNotImplemented  # TODO
