import requests
import configparser
import webbrowser
import numpy as np
import json

class PyStrava:
    def __init__(self):
        self.Config = configparser.ConfigParser()
        self.Config.read('config.ini')
        client_id = self.Config['Authentication']['client_id']
        client_secret = self.Config['Authentication']['client_secret']
        client_code = self.Config['Authentication']['code']
        self.access_token = self.Config['Authentication']['access_token']
        oauth_base = 'https://www.strava.com/oauth/'
        self.api = 'https://www.strava.com/api/v3/'

        if self.access_token:
            return

        if not client_code:
            uri = 'http://lardner.io:8282/authorized'
            request = 'authorize?client_id={}&response_type=code&redirect_uri={}&scope=view_private,write'.format(
                client_id, uri)
            webbrowser.open(oauth_base + request)
        else:
            r = requests.post(oauth_base + 'token',
                              data={'client_id': client_id, 'client_secret': client_secret, 'code': client_code})
            auth_response = json.loads(r.text)
            self.Config.set('Authentication', 'access_token', auth_response['access_token'])
            with open('config.ini', 'w') as configfile:
                self.Config.write(configfile)

    def get_activities(self):
        bearer = 'Bearer {}'.format(self.access_token)
        r = requests.get(self.api + 'athlete/activities', headers={'Authorization': bearer})
        self.activities = json.loads(r.text)

    def set_commute(self, id):
        activiy_string = 'activities/{}'.format(id)
        bearer = 'Bearer {}'.format(self.access_token)
        r = requests.put(self.api + activiy_string, headers={'Authorization': bearer}, data={'commute': 'true'})

    def update_commutes(self):
        self.get_activities()
        Locations = ['Home', 'Work']

        for activity in self.activities:
            Keys = {'Home': False, 'Work': False}
            for Select in Locations:
                d1 = float(self.Config[Select]['lat']) - activity['start_latlng'][0]
                d2 = float(self.Config[Select]['long']) - activity['start_latlng'][1]
                hyp = np.sqrt(d1 ** 2 + d2 ** 2)
                if hyp < 1e-2:
                    Keys[Select] = True

            for Select in Locations:
                d1 = float(self.Config[Select]['lat']) - activity['end_latlng'][0]
                d2 = float(self.Config[Select]['long']) - activity['end_latlng'][1]
                hyp = np.sqrt(d1 ** 2 + d2 ** 2)
                if hyp < 1e-2:
                    Keys[Select] = True

            if all(Keys.values()):
                if not activity['commute']:
                    print('{} is a commute.'.format(activity['id']))
                    print('Updating Strava...')
                    self.set_commute(activity['id'])


if __name__ == '__main__':
    strava = PyStrava()
    strava.update_commutes()
