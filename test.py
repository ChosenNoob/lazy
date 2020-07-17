import multiprocessing

def f(x):
	if x % 2 == 1:
		return x

with multiprocessing.Pool() as pool:
	result = pool.map(f, range(1,20))
	print(result)