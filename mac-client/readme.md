# Micromanage MacOS client

This client esablishes a websocket connection to the backend and will execute task objects that it recieves.

Things to note:
 - DMG install isn't perfect, sometimes fails to unmount, sometimes seems to install corrupt applications.
 - The logging is a bit too verbose.
 - MUST be run as sudo, esp for pkg install.

Things to add:
 - Add sleep state information
 - Better error handling
 - Find different way to check for successful install.
