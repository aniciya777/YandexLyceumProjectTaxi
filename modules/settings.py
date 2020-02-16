import json


class SETTINGS:
    STATUS_CONTEST = 0
    STATUS_FREE = 1
    FIRMS = [
        'Яндекс.Такси',
        'Uber',
        'Rutaxi',
        'Maxim'
    ]
    FPS_COEFF = 0.05
    CELL_SIZE = 100
    CELL_SIZE = (CELL_SIZE, CELL_SIZE * 0.5)

    width = 600
    height = 400
    fullscrean = False
    fps = 60
    status = STATUS_CONTEST
    firm = 0
    points = [0] * len(FIRMS)
    point = 0
    record = 0
    real_width = width
    real_height = height
    fps_real = fps

try:
    config = json.load(open('data/config.json'))
    SETTINGS.status = config['status']
    SETTINGS.firm = config['firm']
    SETTINGS.fps = config['fps']
    SETTINGS.fullscrean = config['fullscreen'] == 'on'
except Exception:
    pass