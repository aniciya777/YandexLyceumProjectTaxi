class SETTINGS:
    STATUS_CONTEST = 0
    STATUS_FREE = 1
    FIRMS = [
        'Яндекс.Такси',
        'Uber',
        'Rutaxi',
        'Maxim'
    ]
    FPS_COEFF = 0.2
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
