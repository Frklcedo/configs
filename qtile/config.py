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

#   #
    # dependencies: firefox nitrogen picom emacs amixer pavucontrol
    #       pcmanfm flameshot
    #       ttf-ubuntu-font-family ttf-font-icons
    # 
    # https://aur.archlinux.org/yay-git.git
    # yay: brave-bin
    # git clone https://git.suckless.org/dmenu

import os
import subprocess
import netifaces
import psutil
import socket
from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
# terminal = guess_terminal()
#terminal = "xfce4-terminal"
#terminal = "st"
terminal = "alacritty"
startupfile = '/.config/qtile/autostart.sh'
defaultcolor = {
    "primary": "#FF8AA9",
    "secondary": "#021526"
}
#fontdefault = "sans"
fontdefault = "Ubuntu"
#fontemoji = "sans"
fontemoji = "FontAwesome all-the-icons"
pclayout = {
    "margin": 12,
    "border_width": 2,
    "border_focus": defaultcolor['primary'],
    "border_normal": defaultcolor['secondary']
}


def get_up_if():
    ifs = netifaces.interfaces()
    for iff in ifs:
        if iff != 'lo':
            interface_addrs = psutil.net_if_addrs().get(iff) or []
            if socket.AF_INET in [snicaddr.family for snicaddr in interface_addrs]:
                return iff
    return "enp20s0"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "o", lazy.layout.grow_main(), desc="over sizing"),
    Key([mod], "y", lazy.layout.shrink_main(), desc="back sizing"),

    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "backslash", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "space", lazy.prev_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # personal configs
    Key([mod, "control"], "x", lazy.screen.next_group(), desc="Go to next group"),
    Key([mod, "control"], "z", lazy.screen.prev_group(), desc="Go to previous group"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="fullscreen window"),

    Key([mod], "c", lazy.spawn("emacsclient -c -a 'emacs'"), desc="emacs"),
    Key([mod], "p", lazy.spawn("dmenu_run -h 20"), desc="dmenu"),
    Key([mod, "mod1"], "f", lazy.spawn("firefox"), desc="Firefox"),
    Key([mod, "mod1"], "b", lazy.spawn("brave"), desc="Brave browser"),
    Key([], "Print", lazy.spawn("flameshot screen -c"), desc="print"),
    Key([mod], "Print", lazy.spawn("flameshot gui"), desc="print gui"),
    Key([mod, "shift"], "d", lazy.spawn("pcmanfm"), desc="pcmanfm"),
    Key([mod, "control"], "v", lazy.spawn("pavucontrol"), desc="audio control"),
]

personalenv = "12345"
groups = [Group(i) for i in personalenv]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(**pclayout),
    layout.Max(**pclayout),
    layout.Floating(**pclayout),
    layout.Matrix(**pclayout),
    layout.MonadWide(**pclayout),
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2, margin=8),
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.RatioTile(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    #layout.Zoomy(),
]


widget_defaults = dict(
    font=fontdefault,
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    foreground="#000000"
                ),
                widget.CurrentLayoutIcon(),
                widget.GroupBox(
                    highlight_method="line",
                    this_current_screen_border=defaultcolor['primary'],
                    this_screen_border=defaultcolor['primary'],
                    highlight_color=['202020'],
                    inactive=['808080'],
                ),
                widget.Prompt(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(),
                widget.Clock(
                    font=f"{fontdefault} Bold",
                    format="%d/%m/%Y %H:%M %p"
                ),
                widget.Spacer(),
                widget.Systray(),
                #widget.Spacer(length=2),
                widget.Net(
                    # interface=['wlp14s0', 'enp20s0'],
                    interface=get_up_if(),
                    font=f"{fontdefault} Bold",
                    padding=12,
                    format='{interface}: {down} ?????? {up}'
                ),
                widget.Sep(
                    background=defaultcolor['primary'],
                    foreground=defaultcolor['primary'],
                ),
                widget.Volume(
                    fmt="\uF028 {}",
                    padding=3,
                    background=defaultcolor['primary'],
                    foreground=defaultcolor['secondary'],
                ),
                widget.Sep(
                    background=defaultcolor['primary'],
                    foreground=defaultcolor['primary'],
                ),
                widget.Sep(
                    foreground='000000',
                ),
                widget.QuickExit(
                    default_text='\uF011',
                    countdown_start=3,
                    countdown_format='{}',
                    font=fontemoji,
                    padding=5
                ),
                widget.Spacer(length=5)
            ],
            20,
            border_width=[0, 2, 0, 0],  # Draw top and bottom borders
            border_color=["000000", defaultcolor["primary"], "ff00ff", defaultcolor["primary"]]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~' + startupfile)
    subprocess.Popen([home])
    # lazy.spawn("nitrogen --restore &")
    # lazy.spawn("picom --experimental-backends --config $HOME/.config/picom/picom.conf &")
