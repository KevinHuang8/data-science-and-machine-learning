import random
import matplotlib.pyplot as plt
import numpy as np

import perceptron_learning_algorithm as PLA

runs = 100
N = 100

def sign(n):
	if n > 0:
		return 1
	elif n < 0:
		return -1
	else:
		return 0

# Target function
def f(x):
	return sign(np.dot(true_weights, x))

# Must be in y = f(x) form, not general form. Given general equatiion
# ax + by + c = 0, corresponding form is y = -a/b*x + c/b
# weights = [c, a, b]
def f_line(x):
	return -(true_weights[1]/true_weights[2]*x) - (true_weights[0]/true_weights[2])

def h_line(w, x):
	return -(w[1]/w[2]*x) - (w[0]/w[2])

def generate_data(N):
	"""generate data based on target function"""
	data = []
	y = []
	for i in range(N):
		x1 = random.uniform(-1, 1)
		x2 = random.uniform(-1, 1)
		y_val = f(np.array([1, x1, x2]))
		y.append(y_val)
		data.append((x1, x2, y_val))
	return data, y

x = np.linspace(-1, 1, 1000)

total_incorrect_in_sample = 0
total_incorrect_out_sample = 0
total_PLA_steps = 0
for i in range(runs):
	# (p, q) and (r, s) = 2 random points on the target function
	p = random.uniform(-1, 1)
	q = random.uniform(-1, 1)
	r = random.uniform(-1, 1)
	s = random.uniform(-1, 1)

	# Weights are the coefficients in ax + by + c = 0 form, so
	# must convert two points into general form.
	# Point slope form: y - y0 = m(x - x0)
	# Converted to general form: -mx + y + (-y0 + m*x0) = 0
	# where m = (q - s)/(p - r), y0 = q, x0 = p
	# Thus, a = -(q - s)/(p - r), b = 1, c = -q + p*(q - s)/(p - r)

	a = -(q - s)/(p - r)
	b = 1
	c = -q + p*(q - s)/(p - r)

	# weights of target function, i.e. target function = ax + by + c
	true_weights = np.array([c, a, b])

	data, y = generate_data(N)

	X = np.array([])
	for x1, x2, _y in data:
		try:
			X = np.vstack((X, np.array([1, x1, x2])))
		except ValueError:
			X = np.array([1, x1, x2])

	X_dagger = np.linalg.pinv(X)
	w = np.matmul(X_dagger, y)


	### Count number of in-sample points that got classified incorrectly

	for x1, x2, _y in data:
		if sign(np.dot(w, np.array([1, x1, x2]))) != _y:
			total_incorrect_in_sample += 1

	### Create out sample test points and see how many are incorretly classified

	out_data, _ = generate_data(1000)

	for x1, x2, _y in out_data:
		if sign(np.dot(w, np.array([1, x1, x2]))) != _y:
			total_incorrect_out_sample += 1

in_sample_error = total_incorrect_in_sample / (runs * N)
print(in_sample_error)

out_sample_error = total_incorrect_out_sample / (runs * 1000)
print(out_sample_error)

average_steps, p_faliure, _w = PLA.percetron_learning_algorithm(N, 100, init_weights=w, 
	in_data=data, visualize=False)
print(average_steps)

### Algorithm Visualization ###		

def plot_points(points):
	"""
	Parameters:
		points - a list of (x, y, sign) tuples

	Plots (x, y) values, with a point being a red circle if 
	the sign is positive, and a blue square if negative.
	"""
	for p in points:
		if p[2] == 1:
			plt.plot(p[0], p[1], 'ro')
		else:
			plt.plot(p[0], p[1], 'bs')

plt.axes(xlim=(-1, 1), ylim=(-1, 1))
plt.plot(x, f_line(x))
plt.plot(x, h_line(w, x))
plot_points(data)
plt.show()