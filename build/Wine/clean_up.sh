#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove other samurai resources
rm -f ./resources/locale/ru/LC_MESSAGES/samurai.mo

# Remove samurai Python files
rm -f ./samurai.py

# Remove shared Python files
rm -f ./{gettext_windows.py,shared.py}

# (Wine-only) Remove build scripts
rm -f ./{build.sh,clean_up.sh,setup.py}

rmdir -p resources/locale/ru/LC_MESSAGES

ls .
