############################################################
# THIS FILE IS USELESS (I THINK ANYWAYS LOL)
############################################################


import requests


class Country:

    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path


class User:

    def __init__(self, name: str, uid: int):
        self._name = name
        self._uid = uid

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_id(self) -> int:
        return self._uid

    def __str__(self):
        return f'{self.name} [{self.user_id}]'


class Time:

    def __init__(self, user: User, time: int):
        self._user = user
        self._time = time

    @property
    def user(self) -> User:
        return self._user

    @property
    def time(self) -> int:
        return self._time

    @property
    def mins(self) -> int:
        return self.time // 60000

    @property
    def secs(self) -> int:
        return (self.time % 60000) // 1000

    @property
    def ms(self) -> int:
        return self.time % 1000

    def __str__(self):
        return f'{self.mins}:{self.secs}.{self.ms} ({self.user})'


class CountryLB:

    def __init__(self, country: Country):
        self._country = country
        self._track_lbs = list()

    @property
    def country(self) -> Country:
        return self._country

    def _load_chart(self, cat: str, track: int):
        url = f'https://www.mkleaderboards.com/api/charts/mkw_{cat}_{self.country.path}/{track+49}'
        r = requests.get(url)
        
        data = r.json()
        times = list()
        for time_data in data['data']:
            user = User(time_data['name'], time_data['player_id'])
            times.append(Time(user, time_data['score']))

        self._track_lbs.append(times)

    def load_times(self):
        for track in range(32):
            self._load_chart('nonsc', track)


class Leaderboard:

    def __init__(self):
        self._countries = list()
        self._countries.append(Country('World', 'world'))
        self._countries.append(Country('United States', 'usa'))
        self._countries.append(Country('Canada', 'canada'))
        self._countries.append(Country('France', 'france'))
        self._countries.append(Country('UK & Ireland', 'ukie'))
        self._countries.append(Country('Spain', 'spain'))
        self._countries.append(Country('Italy', 'italy'))
        self._countries.append(Country('Germany & Austria', 'deat'))
        self._countries.append(Country('Benelux', 'benelux'))
        self._countries.append(Country('Nordic', 'nordic'))
        self._countries.append(Country('Japan', 'japan'))
        self._countries.append(Country('Oceania', 'oceania'))
        self._countries.append(Country('Latin America', 'latam'))
        self._countries.append(Country('Portugal', 'portugal'))

        self._leaderboards = list()
        for country in self._countries:
            self._leaderboards.append(CountryLB(country))


if __name__ == '__main__':
    world = Country('World', 'world')
    worldLB = CountryLB(world)
    worldLB.load_times()
