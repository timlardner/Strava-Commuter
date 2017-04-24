# Strava-Commuter
Determines which rides should be classed as a commute, and does so

### Usage

1. Rename `config.ini.sample` to `config.ini` and populate the client ID and secret with your own details. Fill out the Home and Work information with the latitude and longitude.
2. Import and run PyStrava. The first time this runs, a web browser will open and ask you to authenticate. The callback does not work yet, so copy and paste the code in the URL to the config file.
3. Re-run PyStrava where the code from the previous step will be exchanged for an authentication token. You are now logged in and can run the program.
4. Call the `update_commutes` function which will scan your recent rides. Anything that begins at your home and ends at work (or vice versa) will be tagged as a commute for the world to see.
