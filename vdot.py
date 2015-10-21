from numpy import exp, array, arange


def vdot_raw(distance, seconds):
	"""
		t			: float; sec
		distance	: float; meters
	"""
	if type(distance) == array and type(seconds) == array:
		assert distance.shape == seconds.shape
	d = distance
	t = seconds / 60.0
	A = -4.6
	B = 0.182258
	C = 0.000104
	
	# c(t) or Oxygen Cost
	c = A + B * d / t + C * d**2 / (t**2)
	
	# i(t) or % VO2 Max
	i = 0.8 + 0.1894393 * exp(-0.012778 * t) + 0.2989558 * exp(-0.1932605 * t)
	return c, i

def vdot(distance, seconds):
	"""
		t			: float; sec
		distance	: float; meters
	"""
	c, i = vdot_raw(distance, seconds)
	return c / i


def convert_i(vdot, target_distance, intensity):
	v = vdot
	d = target_distance # meters
	i = intensity

	t = d * 0.004		#start with a reasonable guess
	e = 1.0
	
	for n in xrange(10):
		c = -4.6+.182258*d/t+.000104*d*d/t/t;		#c(t) or Oxygen Cost
#		i = 0.8+.1894393*exp(-.012778*t)+.2989558*exp(-.1932605*t); #i(t) or Intensity
		e = abs(c-i*v);				#distance between curves
		dc = -0.182258*d/t/t-2*.000104*d*d/t/t/t;		#dc(t)/dt or slope of c(t) curve
		di = -0.012778*.1894393*exp(-.012778*t) - 0.1932605*.2989558*exp(-.1932605*t); #di(t)/dt or slope of i(t) curve
		dt = (c-i*v)/(dc-di*v);				#predicted correction
		t -= dt;						#new t value to try
		
		# test for convergence
		if e < 0.01:
			break
	
	return t


def predict(vdot, target_distance):
	v = vdot
	d = target_distance # meters

	t = d*.004						#start with a reasonable guess
	e = 1.0
	
	for n in xrange(10):
		c = -4.6+.182258*d/t+.000104*d*d/t/t;		#c(t) or Oxygen Cost
		i = 0.8+.1894393*exp(-.012778*t)+.2989558*exp(-.1932605*t); #i(t) or Intensity
		e = abs(c-i*v);				#distance between curves
		dc = -0.182258*d/t/t-2*.000104*d*d/t/t/t;		#dc(t)/dt or slope of c(t) curve
		di = -0.012778*.1894393*exp(-.012778*t) - 0.1932605*.2989558*exp(-.1932605*t); #di(t)/dt or slope of i(t) curve
		dt = (c-i*v)/(dc-di*v);				#predicted correction
		t -= dt;						#new t value to try

		# test for convergence
		if e < 0.01:
			break

	return t

assert abs(vdot(3000,600) - 58.849) < 1e-3, "Invalid Vdot %f"  % v


def conv(d, t):
	v = vdot(d, t)
	m,s = divmod(t,60)
	print "%i m in %i:%02i gives vdot=%.2f" % (d,m,s,v)


if __name__ == "__main__":
	d = raw_input("Distance (m) (use suffix k for kilometers)? ").strip()
	if len(d):
		if d[-1].lower() == "k":
			d = float(d[:-1]) * 1000
		elif d[-1].lower() == "mi":
			d = float(d[:-2]) * 1609.344
	print d
	m = raw_input("Minutes? ")
	s = raw_input("Seconds? ")
	conv(float(d), int(m)*60 + int(s))
