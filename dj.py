import time
import pygame
from multiprocessing import Pool, Process
import datetime


def mixer_fadein(fadetime):
    pygame.mixer.music.set_volume(0.0)
    resolution = 0.1#ms
    steps = int(fadetime/resolution)
    inc_per_step = 1.0/steps
    pygame.mixer.music.play()
    for step in range(steps+1):
        pygame.mixer.music.set_volume(step * inc_per_step)
        time.sleep(resolution)
    pygame.mixer.music.set_volume(1.0)

def play(sleeptime, path, length, fadein, fadeout):
    pygame.mixer.init(44100)
    time.sleep(sleeptime)
    pygame.mixer.music.load(path)
    mixer_fadein(fadein)
    time.sleep(length-(fadeout + fadein))
    pygame.mixer.music.fadeout(fadeout*1000)

def play_star(args):
    play(*args)

def print_time():
    t = 0
    while True:
        time.sleep(1.0)
        k = datetime.time(0, t / 60 , t % 60)
        t += 1
        print k.strftime("%M:%S")

if __name__ == '__main__':
    pool = Pool(processes=3)
    pool.map_async(play_star, [
        [0, './long_way_home.mp3', 30, 10, 5],
        [20, './revolution.mp3', 30, 10, 5],
        [40, './get_lucky.mp3', 30, 10, 5],
        ])
    status = Process(target=print_time, args=())
    status.start()
    pool.close()
    pool.join()
