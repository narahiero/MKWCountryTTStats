
import os

import requests


def make_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def mkl_chart_url(cat, chart, track):
    return f'https://www.mkleaderboards.com/api/charts/mkw_{cat}_{chart}/{track}'


if __name__ == '__main__':
    categories = ['combined', 'nonsc']
    charts = [
        'benelux', 'canada', 'deat', 'france', 'italy', 'japan', 'latam',
        'nordic', 'oceania', 'portugal', 'spain', 'ukie', 'usa', 'world'
    ]
    tracks = range(49, 81)

    data_d = make_dir('./data')
    for category in categories:
        cat_d = make_dir(os.path.join(data_d, category))
        for chart in charts:
            chart_d = make_dir(os.path.join(cat_d, chart))
            for track in tracks:
                chart_url = mkl_chart_url(category, chart, track)
                r = requests.get(chart_url)

                track_p = os.path.join(chart_d, str(track) + '.json')
                with open(track_p, 'w') as file:
                    file.write(r.text)
