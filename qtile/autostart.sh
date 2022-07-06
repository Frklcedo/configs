#!/bin/sh
setxkbmap br
nitrogen --restore &
picom --experimental-backends --config $HOME/.config/picom/picom.conf &
