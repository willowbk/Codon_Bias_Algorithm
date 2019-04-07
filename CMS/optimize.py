
def Single_Moves(moves):
	"""
	This function generates a set of all
	possible unique moves in which a single
	parameter is changed in either the 
	positive or negative direction.
	
	Parameters
	----------
		moves : list
		        1-D array of moves represented as characters taking only integer values.
	Returns
	-------
		nns : set
		        A set of all single-move changes to the list move.
	
	"""
	nns = set([])

	for i in range(len(moves)):
		nns.add('_'.join(moves[:i] + [str(int(moves[i]) + 1)] + moves[i+1:]))
		nns.add('_'.join(moves[:i] + [str(int(moves[i]) - 1)] + moves[i+1:]))
		
	return nns



def Get_All_Neighbors(x, dx, depth, min_x, max_x):
	
	"""
	Given that single moves can be generated,
	this function will then construct a set
	of all combinations of single moves 
	up to the value of the parameter 'depth.'
	
	Once the full set of moves are found
	these moves are applied to the current 
	location 
	"""
	
	ns = Single_Moves(['0' for i in range(len(x))])

	for d in range(depth - 1):

		curr_ns = set(ns)
	
		for n in curr_ns:
	
			new_ns = Single_Moves(n.split('_'))
			ns = ns.union(new_ns)
	curr_ns = set(ns)

	for n in curr_ns:
		move_sum = sum([abs(int(move)) for move in n.split('_')])
		if move_sum < depth:
			ns.remove(n)
	
	ns = list(ns)
	ns.sort()
	
	neighbors = [[min([max([float(x[i]) + dx*int(move), min_x[i]]), max_x[i]]) for i,move in enumerate(n.split('_'))] for n in ns]
	
	return neighbors



def CMS(func, init_x, max_x=None, min_x=None, tail=25, tmax=10**3, depth=2, init_dx=None, eps=1e-8):
	
	if max_x == None:
		max_x = [1e16 for i in range(len(init_x))]
		
	if min_x == None:
		min_x = [-1e16 for i in range(len(init_x))]
		
	if init_dx == None:
		init_dx = min([min([max_x[i] - init_x[i], init_x[i] - min_x[i]]) for i in range(len(init_x))])
	
	dx = init_dx
	start_i = 0
	t = 0
	sol_fnd = False

	x = list(init_x)
	F = func(x)
	Ff = 0
	Fs = []

	best_x = list(x)
	best_F = F
	start_F = F
	print('START: ' + str(best_F) + ' ... ' + str(x))

	while t < tmax:
	
		nns = Get_All_Neighbors(x, dx, depth, min_x, max_x)
		min_F = F
		nns_count = 0
		i = start_i
		prev_start_i = start_i
	
		while min_F == F and nns_count < len(nns) and (Ff <= 0 or len(Fs) < tail):
			nn = nns[i]
			min_F = min([func(nn), min_F])
			nns_count += 1
			i = i + 1
			if i >= len(nns):
				i = 0
			t += 1
		
			if len(Fs) == tail:
				Fs = Fs[1:tail + 1]
			Fs.append(F)
		
			Ff = (Fs[-1] - Fs[0])*(tmax - t)/len(Fs) + F 
	
		start_i = i - 1 + int(nns_count == len(nns))
		min_nn = list(nn)
	
		if min_F >= F:
		
			dx /= 2
			if dx < eps:
				dx = init_dx
				sol_fnd = False
			Ff = 0
			Fs = []
		else:
			move = [min_nn[i] - xi for i,xi in enumerate(x)]
			x = list(min_nn)
			F = min_F
		
			itera = 10**6
		
			while itera >= 1:
				new_x = [min([max([x[i] + itera*move[i], min_x[i]]), max_x[i]]) for i in range(len(x))]
				new_F = func(new_x)
				t += 1
			
				if new_F < F:
					x = list(new_x)
					F = new_F
					print('\t F = '+str(F), itera)
				else:
					itera /= 2
				
				Fs.append(F)
		
			sol_fnd = True
	
		if F < best_F:
			print(t, 'BEST: ' + str(func(x)) + ' ... ' + str(x))
		
			best_x = list(x)
			best_F = F
		
	return best_x, best_F




	
	