import optparse
from vdot import *


profiles = {
	"elite": {
		"200m": (200, 1.05, 200),
		"1000m": (1000, 0.98, 1000),
		"VK": (3000, 0.88, 1000),
		"PK": (8000, 0.70, 1000)
	},
	"beginner": {
		"100m": (200, 1.03, 100),		# NK (aerobic)
		"NK": (200, 1.03, 1000),		# NK (aerobic)
		"MK": (1000, 0.95, 1000),	# MK
		"VK": (3000, 0.86, 1000),		# VK
		"PK": (8000, 0.65, 1000)		# PK
	}
}

def s(x):
	return "%d:%02d" % divmod(60*x, 60)

def si(s):
	m, sec = s.split(":")
	return 60 * int(m) + int(sec)


def print_profile_row(t, v, profile):
	trs = [s(convert_i(v, td, ti) / (td/1000.0) * (scale / 1000.0)) for (td,ti,scale) in profile.values()]
	print "%s\t%.2f\t%s" % (s(t/60.0), v, "\t".join(trs))

def print_profile_header(profile):
	print "%im\tvdot\t%s" % (distance, "\t".join(["%s" % k for (k,v) in profile.items()]))


def print_profile(name, profile, ts, distance):
	print
	print "Profile: %s" % name
	print "-" * 24
	
	# print header
	print_profile_header(profile)
	
	for t in ts:
		v = vdot(distance, t)
		print_profile_row(t, v, profile)


def print_profiles(profiles, ts, distance):
	for name, profile in profiles.items():
		print_profile(name, profile, ts, distance)


# args
opts, args = optparse.OptionParser().parse_args()

distance = 1600

# 15 sec bins from 6'00 ... 14'00
table_params = {
	'start':  6,
	'end': 12,
	'step_secs': 10
}

if len(args):
	ts = map(si, args)
	ts.sort()
	print_profiles(profiles, ts, distance)
else:
	start = table_params['start']
	end = table_params['end']
	step = table_params['step_secs']
	ts = [step * t for t in xrange(start * 60 / step, end * 60/step + 1)]
	print_profiles(profiles, ts, distance)

print
for t in ts:
	print "Marathon est. (@%s): %s h" % (s(t/60.0), s(predict(vdot(distance, t), 42195)/60.0))
