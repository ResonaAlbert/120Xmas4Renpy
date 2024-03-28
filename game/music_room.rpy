################################################################################
## MUSIC ROOM DECLARATION
################################################################################
init python:
    #################### STEP 1: Set up the music room.
    ## You can make multiple music rooms consisting of different sets of tracks,
    ## if you so desire, or use one music room for all your music. You only need
    ## to pass in the name of the ExtendedMusicRoom object you set up here to
    ## the music room screens below.

    ## You can pass any of the following arguments to ExtendedMusicRoom:
    ## channel: The channel to play the music on. Defaults to 'music'.
    ## fadeout: The time in seconds to fade out the old song when changing
    ##          tracks. Defaults to 0.0 (no fade).
    ## fadein: The time in seconds to fade in the new song when changing tracks.
    ##         Defaults to 0.0 (no fade).
    ## loop: Whether to loop the music when reaching the end of the track list.
    ##       Defaults to True and can be toggled in the music room with a
    ##       button.
    ## single_track: If True, only a single track will loop. Defaults to False
    ##               and can be toggled in the music room with a button.
    ## shuffle: Whether to shuffle the tracks or play them in default order.
    ##          Defaults to False and can be toggled in the music room with a
    ##          button.
    ## stop_action: A screen action to run when the music stops. Defaults to
    ##              None, so no action is run.
    ## alphabetical : If True, the tracks will be sorted alphabetically.
    ##                If False, the default, they will be arranged in the order
    ##                they are added to the music room in.
    music_room = ExtendedMusicRoom(channel='music', fadeout=0.0, fadein=0.0,
        loop=True, single_track=False, shuffle=False, stop_action=None,
        alphabetical=False)

    ## This sets up a default art image for all tracks in this room which aren't
    ## given a more specific one. This default art is 600x600, but several
    ## layouts resize it. It should typically be square.
    music_room.default_art = "gui/music_room/cover_art.webp"

    ## Now you can declare the music files. These will appear in the music room
    ## in the order you declare them in, unless you set alphabetical=True above.
    music_room.add(
        ## The title of the song. Used for alphabetization. Should probably
        ## be translatable.
        name=_("Theme"),
        ## This should be the path to the song i.e. "audio/music/sugar_plum.ogg"
        path="audio/BGM/Theme2.mp3",
        ## The song artist. Optional; depends on how you want to set up
        ## your screens. The default layouts use the artist field.
        artist="Guke",
        ############ The following are more optional fields ####################
        ## This can be the path to album art specific for this song. If not
        ## provided/it is None (the default), it'll use the default_art,
        ## provided above. You can provide Null() if you'd like no image at all,
        ## not even the default.
        art=None,
        ## An optional extra field. You can put whatever information you like
        ## in here and display it however you want in the music room screen.
        ## By default, the screens do not display this information.
        description=_("From {i}The Nutcracker{/i}"),
        ## You may optionally provide an unlock condition as a string, which
        ## will be evaluated to determine if the song is unlocked or not.
        ## In this case, the song is unlocked when the persistent variable
        ## persistent.watched_intro is True.
        ## By default, songs are unlocked when the player has listened to them
        ## in-game. You can also set this to "True" to have a song be always
        ## unlocked.
        unlock_condition="persistent.watched_intro",
    )


################################################################################
## CONFIGURATION VALUES
################################################################################
## Set this to True if you want to unlock all tracks in the music room during
## development. Set it to False to test the unlock conditions. Tracks will
## automatically obey unlock rules in a distribution regardless of the value
## of this configuration variable.
define myconfig.UNLOCK_TRACKS_FOR_DEVELOPMENT = True

################################################################################
## IMAGES & DEFINITIONS
################################################################################
## These colours are used by the colorize_button transform in the screens below
## to colorize the default music controls. You can change these if you want to
## use the provided images, or simply supply your own and remove the lines
## `at colorize_button` from the screen below.
define MUSIC_ROOM_IDLE_COLOR = '#ffffff'
define MUSIC_ROOM_HOVER_COLOR = "#597FB3"
define MUSIC_ROOM_SELECTED_IDLE_COLOR = '#ffffff'
define MUSIC_ROOM_SELECTED_HOVER_COLOR = "#597FB3"
define MUSIC_ROOM_INSENSITIVE_COLOR = "#888"

## Here are the default buttons used for the music controls below. You can
## update these or replace them.
image play_button = "gui/music_room/play.webp"
image pause_button = "gui/music_room/pause.webp"
image next_button = "gui/music_room/next.webp"
image prev_button = Transform("gui/music_room/next.webp", xzoom=-1.0)
image repeat_all_button = "gui/music_room/repeat all.webp"
## Note that this image is just a foreground on top of the repeat_all button!
image repeat_one_button = "gui/music_room/repeat 1.webp"
image shuffle_button = "gui/music_room/shuffle.webp"
image back_10_button = "gui/music_room/back_10.webp"
image forward_10_button = "gui/music_room/forward_10.webp"

## The "audio level" bars. These are optional to show next to the currently
## playing song. There are four bars that randomly change height.
define AUDIO_BAR_HEIGHT = 30
define AUDIO_BAR_WIDTH = 8
image audio_bar = Transform(MUSIC_ROOM_HOVER_COLOR,
    xysize=(AUDIO_BAR_WIDTH, AUDIO_BAR_HEIGHT))
transform audio_bar_move():
    yzoom renpy.random.random() ## Start at a random height
    block:
        ## Choose a random height to be
        choice:
            ease 0.2 yzoom 1.0
        choice:
            ease 0.2 yzoom 0.2
        choice:
            ease 0.2 yzoom 0.8
        choice:
            ease 0.2 yzoom 0.0
        choice:
            ease 0.2 yzoom 0.5
        repeat
## The final audio bars image, with four bars that randomly change height.
image audio_bars = HBox(
    At('audio_bar', audio_bar_move),
    At('audio_bar', audio_bar_move),
    At('audio_bar', audio_bar_move),
    At('audio_bar', audio_bar_move),
    yalign=1.0, ysize=AUDIO_BAR_HEIGHT,
)

################################################################################
## TRANSFORMS
################################################################################
## A transform that makes it easier to apply colours to the various buttons.
## The default images are black, so it uses ColorizeMatrix to colorize them.
## The colours are defined at the top of the file.
transform colorize_button(idle=MUSIC_ROOM_IDLE_COLOR,
        hover=MUSIC_ROOM_HOVER_COLOR,
        selected_idle=MUSIC_ROOM_SELECTED_IDLE_COLOR,
        selected_hover=MUSIC_ROOM_SELECTED_HOVER_COLOR,
        insensitive=MUSIC_ROOM_INSENSITIVE_COLOR):
    matrixcolor ColorizeMatrix(insensitive, "#fff")
    on idle:
        matrixcolor ColorizeMatrix(idle, "#fff")
    on hover:
        matrixcolor ColorizeMatrix(hover, "#fff")
    on insensitive:
        matrixcolor ColorizeMatrix(insensitive, "#fff")
    on selected_idle:
        matrixcolor ColorizeMatrix(selected_idle, "#fff")
    on selected_hover:
        matrixcolor ColorizeMatrix(selected_hover, "#fff")

## A simple transform to easily resize buttons. Used by some layouts.
transform zoom_button(z):
    zoom z

style music_room_pos:
    color "#fff" xalign 0.5 adjust_spacing False
style music_room_duration:
    color "#fff" xalign 0.5 adjust_spacing False

################################################################################
## Styles for the track list, shared generally by the other rooms.
################################################################################
style track_list_frame:
    yalign 0.0 xalign 0.0
    padding (25, 25)
style track_list_vbox:
    spacing 0
style track_list_button:
    xsize 400
    ysize 120
    background Frame("gui/music_room/music_btn_idle.png", tile=False)
    hover_background Frame("gui/music_room/music_btn_hover.png", tile=False)
    selected_background Frame("gui/music_room/music_btn_selected.png", tile=False)

style track_list_button_text:
    xalign 0.5
    color "#597FB3" hover_color '#ffffff' selected_color "#597FB3" 
    insensitive_color "#666"


#### main music room #######
################################################################################
## SCREENS - VERSION 3
################################################################################
screen music_room3(mr):

    tag menu

    ## Needed to have easy access to information on the currently playing song.
    ## Required for ALL music rooms!
    default current_track = mr.get_current_song()

    style_prefix "music_room3"

    add gui.game_menu_background

    ############################################################################
    ## If you have a standard Ren'Py UI sidebar, you can use this:
    ##
    # use game_menu(_("Music Room")):
    ##
    ## Otherwise, if you're using my Easy Ren'Py GUI (https://feniksdev.itch.io/easy-renpy-gui)
    ## you can use this:
    ##
    imagebutton auto "gui/button/Back_Bar_%s.png":
        xalign 0.0
        yalign 0.5
        action Return()
        activate_sound "audio/click2.mp3" 

    fixed:
        yfill True
        xsize config.screen_width-200
        align (1.0, 0.5)
    ##
    ############################################################################

        frame:
            style_prefix 'track_list'
            xfill True top_margin 0 yfill True bottom_margin 300 left_margin 20 right_margin 0
            hbox:
                grid 4 7:
                    xfill True
                    yfill True
                #    spacing 4
                    ## Track info
                    for num, song in enumerate(mr.get_tracklist(all_tracks=True)):
                        textbutton(song.name):
                            action mr.Play(song.path)
                    #    text song.artist

            #imagebutton auto "gui/music_room/music_btn_%s.png"

        ## This holds the album art, song title, artist, music bar, and music
        ## controls. You may adjust this however you wish! The important part
        ## is generally the actions on the buttons, and the music bar is special
        ## so you can click it to seek in the song.
        frame:
            style_prefix 'musicroom3'
            has hbox
            xalign 0.5 yalign 0.5
            if current_track:
                add current_track.art ysize 150 fit "contain"
            else:
                add mr.default_art ysize 150 fit "contain"
            vbox:
                xsize 150
                if current_track:
                    text current_track.name
                #    text current_track.artist color "#112d6a"
                else:
                    text _("No song playing")

            null width 10

            vbox:
                yalign 0.5 spacing 15
                hbox:
                    xalign 0.5 spacing 40
                    ################## Shuffle button ##################
                    imagebutton:
                        idle "shuffle_button"
                        at colorize_button(MUSIC_ROOM_INSENSITIVE_COLOR,
                            MUSIC_ROOM_IDLE_COLOR), zoom_button(0.6)
                        action mr.ToggleShuffle()
                    ############ Previous, play/pause, next buttons ############
                    imagebutton:
                        idle "prev_button"
                        at colorize_button(), zoom_button(0.4)
                        action mr.Previous()
                    imagebutton:
                        at colorize_button(), zoom_button(0.25)
                        idle "pause_button" hover "pause_button"
                        selected_idle "play_button" selected_hover "play_button"
                        action mr.PlayAction()
                    imagebutton:
                        idle "next_button"
                        at colorize_button(), zoom_button(0.4)
                        action mr.Next()
                    ################## Repeat all, repeat one buttons ##################
                    imagebutton:
                        at colorize_button(idle=MUSIC_ROOM_INSENSITIVE_COLOR,
                            hover=MUSIC_ROOM_IDLE_COLOR), zoom_button(0.6)
                        idle "repeat_all_button"
                        if mr.single_track:
                            foreground "repeat_one_button"
                        action mr.CycleLoop()

                ################## Music Bar ##################
                hbox:
                    spacing 8
                    fixed:
                        yfit True xsize 200
                        add mr.get_pos(style="music_room_pos")
                    music_bar room mr
                    fixed:
                        yfit True xsize 200
                        add mr.get_duration(style="music_room_duration")

            add "gui/music_room/volume.webp" zoom 0.45 yalign 0.5:
                matrixcolor ColorizeMatrix(MUSIC_ROOM_HOVER_COLOR, "#112d6a")

            bar value MixerValue(mr.channel) xysize (200, 25):
                xalign 0.5 right_bar '#ffffff' thumb None yalign 0.5
                left_bar "#597FB3"

style musicroom3_frame:
    yalign 1.0 xalign 0.5 
    xoffset 20 yoffset 20
    xfill True 
    ysize 300
    background Frame(["gui/music_room/music_room_play_frame.png"])

style musicroom3_hbox:
    spacing 20
style musicroom3_image_button:
    yalign 0.5
style musicroom3_bar:
    ysize 25 xsize 480
    yalign 0.5
    right_bar '#ffffff' thumb None
    left_bar "#597FB3"
style musicroom3_text:
    yalign 0.5 size 35 color '#ffffff'
style musicroom3_vbox:
    yalign 0.5