#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir -p ./resources/locale/ru/LC_MESSAGES/

# Copy other samurai resources
cp -u /usr/local/bin/samurai/resources/locale/ru/LC_MESSAGES/samurai.mo ./resources/locale/ru/LC_MESSAGES/

# Copy samurai Python files
cp -u /usr/local/bin/samurai/src/samurai.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/src/{gettext_windows.py,shared.py} .

# (Linux-only) Copy build scripts
cp -u /usr/local/bin/samurai/build/Linux/{build.sh,clean_up.sh,setup.py} .

ls .
