class Track:
    def __init__(self, path,
            start_offset=0, length=30,
            crossfade_time=10,
            bpm=128,
            key="Amin"):
        self.path = path
        self.start_offset = start_offset
        self.length = length
        self.crossfade_time = crossfade_time
        self.bpm = bpm
        self.key = key
