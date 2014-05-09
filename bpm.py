from track import Track
import itertools
from sys import argv

def antuanThingy(perm):
	pass

def slope(tracks):
	y = tracks
	N = len(y)
	x = range(N)
	B = (sum(x[i] * y[i] for i in xrange(N)) - 1./N*sum(x)*sum(y)) / (sum(x[i]**2 for i in xrange(N)) - 1./N*sum(x)**2)
	return B


def getTrackList(tracks):
	permutations = itertools.permutations(tracks, len(tracks))
	permValues = []
	increasingPermutations = (s for s in permutations if slope(s) >= 0)
	for permutation in increasingPermutations:
		diffs = (abs(l - r) for l, r in itertools.izip(permutation, permutation[1:]))
		penalized = (v if v != 0 else 2 for v in diffs)
		total = sum(penalized)
		permValues.append((total, permutation))
		minValue, minPermutation = min(permValues, key=lambda x:x[0])
	
	return minPermutation

def trackWrapper(tracks):
	bpms = []
	for track in tracks:
		bpms.append(track.bpm)
	newTracks = []
	bpmOrder = getTrackList(bpms)
	for bpm in bpmOrder:
		for t in tracks:
			if t.bpm == bpm:
				newTracks.append(t)
				tracks.remove(t)
	return newTracks		

if __name__ == '__main__':
	l =' '.join(argv[1:])
	#print trackWrapper(eval(l))
	newTracks = trackWrapper(tracks)
	for x in newTracks:
		print x.bpm
