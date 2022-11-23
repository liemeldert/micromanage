# Micromanage MacOS client

This client esablishes a websocket connection to the backend and will execute task objects that it recieves.

Things to note:
 - DMG install isn't perfect, sometimes fails to unmount, sometimes seems to install corrupt applications.
 - The logging is a bit too verbose.
 - MUST be run as sudo, esp for pkg install.
