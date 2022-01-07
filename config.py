# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from os import path
import subprocess

# Definimos el path local
local_path = path.join(path.expanduser('~'), '.config', 'qtile')

# Definimos tamaños de letra
base_fontsize = 14
delta_font = 2

s3small_fontsize = base_fontsize - 3*delta_font
s2small_fontsize = base_fontsize - 2*delta_font
small_fontsize   = base_fontsize - delta_font
normal_fontsize  = base_fontsize
big_fontsize     = base_fontsize + delta_font
s2big_fontsize   = base_fontsize + 2*delta_font
s3big_fontsize   = base_fontsize + 3*delta_font

# Definimos colores para usar en el script (cada color es una lista de dos -> degradados)
colors_codes = {
    "deg": "#0f111a",
    "dark": "#0f101a",
    "ligth": "#f1f1f1",
    "text": "#fffeec",
    "grey": "#606060",
    "grey_dark": "#505050",
    "magenta": "#d8555d",
    "red": "#da3942",
    "red_dark": "#770000",
    "orange": "#fb9f7f",
    "golden": "#ffd47e",
    "purple": "#660066",    
    "purple_dark": "#330033",    
    "green": "#00bb55",
    "green_dark": "#11aa00",
    "blue": "#29397a",
    "yellow": "#ffff33",
    "yellow_dark": "#cccc00",
}

colors = {}

for color in colors_codes:
    tmp_colors = [
        color,
        color + '_deg'
    ]

    for tmp_color in tmp_colors:
        if '_deg' in tmp_color:
            c1 = colors_codes['deg']
        else:
            c1 = colors_codes[color]

        c2 = colors_codes[color]

        colors[tmp_color] = [
            c1,
            c2,
        ]

# Creamos degradados monocolor
colors['green_monodeg'] = [
    colors_codes['green_dark'],
    colors_codes['green'],
]

colors['red_monodeg'] = [
    colors_codes['red_dark'],
    colors_codes['red'],
]

colors['yellow_monodeg'] = [
    colors_codes['yellow_dark'],
    colors_codes['yellow'],
]

colors['purple_monodeg'] = [
    colors_codes['purple_dark'],
    colors_codes['purple'],
]

# Elegimos el color FOCUS
colors['focus'] = colors['purple_monodeg']
colors['focus_alt'] = colors['purple_deg']
colors['selected_window'] = colors['red_dark']

# colors['focus'] = colors['red_monodeg']
# colors['focus_alt'] = colors['green_monodeg']

# Configuramos los separadores que se crearán
separators = {
    "color": [
        colors['focus_alt'],
        colors['focus'],
    ],
    "padding": [
        10,
        10
    ],
}

# Congiguramos las imagenes complementarias que se crearán
images = {
    "color": [
        colors['focus'],
        colors['focus'],
        colors['focus_alt'],  
    ],
    "filename": [
        path.join(local_path, 'img', 'bar_dark_grey.png'),
        path.join(local_path, 'img', 'bar_dark_red.png'),
        path.join(local_path, 'img', 'bar_dark_red.png'),
    ],
}

# Lanzamos el autostart.sh solo una vez
@hook.subscribe.startup_once
def autostart():
    subprocess.call(path.join(local_path, 'autostart.sh'))

# mod = "mod1" # Alt
mod = "mod4" # Windows
terminal = "alacritty"




# ----------------- KEYS -----------------

keys = [
    # -------------- Window config --------------
    # Switch between windows
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), 
        desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), 
        desc="Grow window up"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    # -------------- Program config --------------
    # Launch terminal
    Key([mod], "Return", lazy.spawn(terminal), desc=terminal),

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show run")),

    # Window tab
    Key([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Firefox
    Key([mod], "f", lazy.spawn("firefox")),

    # Opera
    Key([mod], "o", lazy.spawn("opera")),


    # VSCode
    Key([mod], "c", lazy.spawn("code")), 

    # Scrot
    Key([mod], "s", lazy.spawn("scrot")),

    # Thunder
    Key([mod], "e", lazy.spawn("thunar")),


    # -------------- Hardware config --------------
    # Volume control
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),    
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn(
        "brightnessctl set +10%"
    )),    
    Key([], "XF86MonBrightnessDown", lazy.spawn(
        "brightnessctl set 10%-"
    )),     
]

# ----------------- GROUPS -----------------

#group_names = ["MAIN", "WWW", "DEV", "MISC", "FOLDER"]
group_names = ["   ", "   ", "   ", "   ", "   "]

groups = [Group(i) for i in group_names]

for i,group in enumerate(groups):
    actual_key = str(i + 1)

    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),

        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name)),
    ])

dgroups_key_binder = None
dgroups_app_rules = []  # type: List

# ----------------- LAYOUTS -----------------

layout_conf = {
    'border_focus': colors['selected_window'][0],
    'border_width': 2,
    'margin': 4
}

layouts = [
    #layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

#floating_layout = layout.Floating(
#    float_rules = [
#        # Run the utility of `xprop` to see the wm class and name of an X client.
#        {'wmclass': 'confirm'},
#        {'wmclass': 'dialog'},
#        {'wmclass': 'download'},
#        {'wmclass': 'error'},
#        {'wmclass': 'file_progress'},
#        {'wmclass': 'notification'},
#        {'wmclass': 'splash'},
#        {'wmclass': 'toolbar'},
#        {'wmclass': 'confirmreset'}, # gitk
#        {'wmclass': 'makebranch'}, # gitk
#        {'wmclass': 'maketag'}, # gitk
#        {'wmname': 'branchdialog'}, # gitk
#        {'wmname': 'pinentry'}, # GPG key password entry
#        {'wmname': 'ssh-askpass'}, # ssh-askpass
#    ], 
#    border_focus = colors['selected_window'][0]
#)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


# ----------------- WIDGETS -----------------

widget_defaults = dict(
    padding = 3,
    font = "UbuntuMono Nerd Font",
    fontsize = normal_fontsize,
)
extension_defaults = widget_defaults.copy()

# Creamos los widget separadores según configuración
sep = []
for i, sep_color in enumerate(separators['color']):
    new_sep =  widget.Sep(
        linewidth = 0, 
        padding = separators['padding'][i], 
        background = separators['color'][i]
    )
    sep.append(new_sep)

img = []
for i, img_color in enumerate(images['color']):
    new_img = widget.Image(
        backgroud = images['color'][i],
        filename = images['filename'][i],
    )

    img.append(new_img)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    padding_x = 5,
                    padding_y = 8,
                    borderwidth = 3,
                    rounded = True,
                    background = colors['dark'],
                    foreground = colors['dark'],
                    active = colors['ligth'],
                    inactive = colors['grey'],
                    highlight_method = 'block',
                    font = "UbuntuMono Nerd Font",
                    fontsize = normal_fontsize,
                    center_aligned = True,
                    this_current_screen_border = colors['focus'],
                    this_screen_border = colors['grey'],
                    other_current_screen_border = colors['dark'],
                    other_screen_border = colors['dark']
                ),
                widget.WindowName(
                    background = colors['dark'],
                    foreground = colors['focus'],
                    fontsize = small_fontsize,
                    font = "UbuntuMono Nerd Font Bold"
                ),
                img[0],
                sep[1],
                widget.Systray(
                    padding = 20,
                    background = colors['focus'],
                    foreground = colors['text'],                    
                ),
                sep[1],
                img[0],
                sep[0],
                widget.CurrentLayoutIcon(
                    padding = 8,
                    background = colors['focus_alt'],
                    foreground = colors['text'],
                    scale = 0.6
                ),
                widget.CurrentLayout(
                    padding = 20,
                    background = colors['focus_alt'],
                    foreground = colors['text'], 
                    font = "UbuntuMono Nerd Font",
                    fontsize = normal_fontsize                   
                ), 
                sep[0], 
                img[0],
                sep[1], 
                widget.TextBox(
                    background = colors['focus'],
                    foreground = colors['text'],
                    text = ' 﨟  ',
                    fontsize = s2big_fontsize
                ),           
                widget.Clock(
                    padding = 15,
                    background = colors['focus'],
                    foreground = colors['text'],
                    format = "%Y-%m-%d %H:%M",
                    font = "UbuntuMono Nerd Font",
                    fontsize = normal_fontsize,
                    ),
            ],
            28,
            opacity=0.75
        ),
    ),
]

# ----------------- MOUSE -----------------

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False


# ----------------- OTHERS -----------------

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
