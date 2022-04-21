
import json
from typing import List, Tuple
import os


class Player:

    def __init__(self, name: str, id: int):
        self._name = name
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id


class Time:

    def __init__(self, player: Player, time: int):
        self._player = player
        self._time = time

    @property
    def player(self) -> Player:
        return self._player

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


class ChartTrack:

    def __init__(self, chart, track: int):
        self._chart = chart
        self._track = track
        self._times = list()
        self._time_avg = 0
        self._players = list()

    @property
    def chart(self):
        return self._chart

    @property
    def track(self) -> int:
        return self._track

    @property
    def times(self) -> List[Time]:
        return self._times

    @property
    def top(self) -> Time:
        return self.times[0]

    @property
    def bottom(self) -> Time:
        return self.times[-1]

    @property
    def avg(self) -> int:
        return self._time_avg

    def top_avg(self, count: int = -1) -> int:
        if count == -1:
            count = len(3 if len(self.times) == 10 else 2)

        total_time = 0
        for i in range(count):
            total_time += self.times[i].time
        return total_time // count

    def bottom_avg(self, count: int = -1) -> int:
        if count == -1:
            count = len(3 if len(self.times) == 10 else 2)

        total_time = 0
        for i in range(count):
            total_time += self.times[-i-1].time
        return total_time // count

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def path(self) -> str:
        return os.path.join(self.chart.id.path, f'{self.track+49}.json')

    def load(self):
        if len(self.times) > 0:
            return

        with open(self.path, 'r') as file:
            data = json.load(file)
            total_time = 0
            for time_data in data['data']:
                player = Player(time_data['name'], time_data['player_id'])
                time = Time(player, time_data['score'])
                self.times.append(time)
                self.players.append(player)
                total_time += time.time
            self._time_avg = total_time // len(self.times)


class ChartID:

    def __init__(self, cat: str, chart: str):
        self._cat = cat
        self._chart = chart

    @property
    def cat(self) -> str:
        return self._cat

    @property
    def chart(self) -> str:
        return self._chart

    @property
    def path(self) -> str:
        return f'./data/{self.cat}/{self.chart}/'


class Chart:

    def __init__(self, id: ChartID):
        self._id = id
        self._tracks = list()
        self._players = list()

    @property
    def id(self) -> ChartID:
        return self._id

    @property
    def tracks(self) -> List[ChartTrack]:
        return self._tracks

    @property
    def players(self) -> List[Player]:
        return self._players

    def load(self):
        if len(self.tracks) > 0:
            return

        for id in range(32):
            track = ChartTrack(self, id)
            track.load()
            self.tracks.append(track)

            new_players = list()
            for player in track.players:
                unique = True
                for player_c in self.players:
                    if player.id == player_c.id:
                        unique = False
                        break
                if unique:
                    new_players.append(player)

            self.players.extend(new_players)


class ChartManager:

    def __init__(self, charts: List[str]):
        self._world_chart = Chart(ChartID('nonsc', 'world'))
        self._charts = list()
        self._chart_names = charts
        for name in self.chart_names:
            self._charts.append(Chart(ChartID('nonsc', name)))

        self._track_ranges = list()

    @property
    def world_chart(self) -> Chart:
        return self._world_chart

    @property
    def charts(self) -> List[Chart]:
        return self._charts

    @property
    def chart_names(self) -> List[str]:
        return self._chart_names

    @property
    def track_ranges(self) -> List[Tuple[int, int]]:
        return self._track_ranges

    def calc_score(self, track: int, time: int) -> float:
        r = self.track_ranges[track]
        t = time - r[0]
        return t / r[1]

    def load(self):
        self.world_chart.load()
        for chart in self.charts:
            chart.load()

        for i in range(32):
            top_t = self.world_chart.tracks[i].top.time
            bottom_t = 0
            for chart in self.charts:
                track = chart.tracks[i]
                bottom_t = max(bottom_t, track.bottom.time)
            track_range = (top_t, bottom_t - top_t)
            self.track_ranges.append(track_range)


###############################################################################


def get_charts():
    return [
        'usa',
        'canada',
        'france',
        'ukie',
        #'spain',
        #'italy',
        'deat',
        'benelux',
        'nordic',
        'japan',
        'oceania',
        'latam',
        #'portugal'
    ]


def time_str(time: int):
    return f'{time//60000}:{((time%60000)//1000):02d}.{(time%1000):03d}'


if __name__ == '__main__':
    manager = ChartManager(get_charts())
    manager.load()

    chart_scores = dict()
    for chart in manager.charts:
        avg_add = 0.0
        top_add = 0.0
        bottom_add = 0.0
        for t in range(32):
            track = chart.tracks[t]
            avg_add += manager.calc_score(t, track.avg)
            top_add += manager.calc_score(t, track.top.time)
            bottom_add += manager.calc_score(t, track.bottom.time)
        avg_score = avg_add / 32
        top_score = top_add / 32
        bottom_score = bottom_add / 32

        chart_scores[chart.id.chart] = (len(chart.players), avg_score, top_score, bottom_score)

    ordered_charts = list()
    cmp = 1
    for chart_score in chart_scores:
        index = 0
        for chart in ordered_charts:
            if chart_scores[chart_score][cmp] < chart_scores[chart][cmp]:
                break
            index += 1
        ordered_charts.insert(index, chart_score)

    print(f'\n  # |{"CHART":^10}|{"PLAYERS":^10}|{"AVERAGE":^10}|{"TOP":^10}|{"BOTTOM":^10}')
    print('-'*59)
    pos = 1
    for chart in ordered_charts:
        score = chart_scores[chart]
        print(f' {pos:>2} | {chart:<9}|  {score[0]:^8}|  {score[1]:.4f}  |  {score[2]:.4f}  |  {score[3]:.4f}')
        pos += 1
