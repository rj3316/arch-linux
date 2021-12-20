#!/bin/bash

rm ~/.local/share/qtile/qtile.log.old 2> /dev/null

cp ~/.local/share/qtile/qtile.log ~/.local/share/qtile/qtile.log.old

echo "" > ~/.local/share/qtile/qtile.log
