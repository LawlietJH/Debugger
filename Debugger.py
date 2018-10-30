
# Decoradores para depurar funciones.
# Debugger.py
# Python 3
# By: LawlietJH
# - - - v1.2.4


import functools
import time
import sys


#======================================================================= 
#Variables Globales:

nivelProfundidad = 0

#======================================================================= 
#Se utiliza como @timeSleep(parámetros)
# 
# Parámetros:
# 
# tmp  = tiempo que durara la pausa. Este valo puede ir desde 0.01 en adelante.
# 
# show = si es True mostrara una cadena en pantalla con la palabra "Espere..."
#        y si es False, no imprimira nada.
# 
def timeSleep(tmp=1, show=False):				# Recibe los parametros del decorador.
	""" Esta funcion (Decorador) sirve para hacer una pausa al terminar
		la funcion a decorar, que puede ser desde 0.01 segundos en adelante. """
	def fTimeSleep(func):						# Recibe la Función.
		
		global nivelProfundidad
		nivelProfundidad += 1
		
		@functools.wraps(func)					# Coloca a la Función como principal y no al decorador.
		def fArgs(*args, **kwargs):				# Recibe los parametros de la funcion.
			valores = func(*args, **kwargs)
			print()
			for num in range(int(tmp*100)):
				time.sleep(.01)
				if show: sys.stdout.write(f'\r Esperando ... {tmp-(num/100):.2f}\t')
			sys.stdout.write('\r\t\t\t\n')
			return valores
		
		return fArgs
	return fTimeSleep
#=======================================================================

#======================================================================= 
#Se utiliza como: @lowerCase
def lowerCase(func):						# Recibe la Función.
	""" Esta funcion (Decorador) sirve para poner en minusculas todos
		los caracteres en la variables dentro de la funcion a decorar. """
	@functools.wraps(func)					# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):				# Recibe los parametros de la funcion.
		
		global nivelProfundidad
		nivelProfundidad += 1
		
		def rec(vals, tipo=None):
			
			rargs = []
			if tipo == dict():
				for b, a in vals.items():
					if   type(a).__name__ == 'list':  a = rec(a, list())
					elif type(a).__name__ == 'tuple': a = rec(a, tuple())
					elif type(a).__name__ == 'dict':  a = rec(a, dict())
					try: rargs = {b.lower():a.lower()}
					except: rargs = {b.lower():a}
			else:
				for a in vals:
					if   type(a).__name__ == 'list':  a = rec(a, list())
					elif type(a).__name__ == 'tuple': a = rec(a, tuple())
					elif type(a).__name__ == 'dict':  a = rec(a, dict())
					try: rargs.append(a.lower())
					except: rargs.append(a)
				if tipo == tuple(): rargs = tuple(rargs)
			return rargs
		
		rargs = rec(args)
		valores = func(*rargs, **kwargs)
		
		return valores
	return fArgs
#=======================================================================

#=======================================================================
#Se utiliza como: @timer
def timer(func):						# Recibe la Función.
	""" Esta funcion (Decorador) permite contar el tiempo de ejecucion
		de la funcion a decorar, desde el momento en que se ejecuta
		hasta que termine su ejecucion de dicha funcion. """
	@functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):			# Recibe los parametros de la funcion.
		
		global nivelProfundidad
		nivelProfundidad += 1
		
		tmp_ini = time.perf_counter()		# Obtiene el Tiempo actual antes de correr la función.
		valores = func(*args, **kwargs)		# Ejecuta la Función.
		tmp_fin = time.perf_counter()		# Obtiene el Tiempo actual despues de correr la función.
		tmp_tot = tmp_fin - tmp_ini			# Calcula el tiempo transcurrido.
		
		print(f'\n [+] Función \'{func.__name__}()\' Terminada en {tmp_tot:.4f} segundos.\n')
		
		return valores
	return fArgs
#=======================================================================

#=======================================================================
#Se utiliza como: @counter
def counter(func):
	""" Esta funcion (Decorador) permite contar e imprímir el número de
		veces que la función a decorar ha sido ejecutada. """
	@functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):			# Recibe los parametros de la funcion.
		
		global nivelProfundidad
		nivelProfundidad += 1
		
		fArgs.count = fArgs.count + 1
		valores = func(*args, **kwargs)
		
		print(f'\n [+] La Función \'{func.__name__}()\' Ha Sido Utilizada {fArgs.count} veces.\n')
		
		return valores
	fArgs.count = 0
	return fArgs
#=======================================================================

#=======================================================================
#Se utiliza como: @debug
def debug(func):						# Recibe la Función.
	""" Esta funcion (Decorador) permite observar con presicion los
		valores de entrada y salida de la funcion a decorar. """
	@functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):			# Recibe los parametros de la funcion.
		
		global nivelProfundidad
		nivelProfundidad += 1
		
		rargs   = [repr(a) for a in args]
		rkwargs = [f'{k}={v!r}' for k, v in kwargs.items()]
		rArgs   = ', '.join(rargs + rkwargs)
		
		valores = func(*args, **kwargs)
		
		print(f'\n [+] Función y Parámetros: {func.__name__}({rArgs})\n [+] Devuelve: {valores!r}\n')
		
		return valores
	return fArgs
#=======================================================================

#=======================================================================
#Se utiliza como: @symbolsTable
class symbolsTable(object):
	global nivelProfundidad
	def __init__(self, func):
		
		self._locals = []
		self.func = func
	
	def __call__(self, *args, **kwargs):
		
		global nivelProfundidad
		# Contara cuantos decoradores hay debajo de este, para seleccionar
		# los elementos de la ultima funcion (la funcion a decorar).
		nivelProfundidad = 1
		
		def tracer(frame, event, arg):
			if event=='return':
				self._locals.append(frame.f_locals.copy())
		
		sys.setprofile(tracer)
		try: valores = self.func(*args, **kwargs)
		finally: sys.setprofile(None)
		
		self.locals					# Imprime La Tabla de Símbolos de la Función Indicada.
		
		return valores
	
	@property
	def __name__(self):				# Coloca a la Función como principal y no al decorador.
		return self.func.__name__
	
	@property						# permite ejecutar la funcion 'self.locals()' como 'self.locals'.
	def locals(self):
		print(f'\n [+] Tabla de Símbolos en la función \'{self.func.__name__}()\':\n')
		for i, (x, y) in enumerate(self._locals[-nivelProfundidad].items()):
			print(f'\t [{i+1}]: {x} = {y}')
		print('')
#=======================================================================



#=======================================================================

# Los decoradores se van ejecutando en orden ascendente (de abajo hacia
# arriba)a partir de la funcion a decorar, por esto, se otorgo un orden
# de prioridad tomando en cuenta la funcion de cada decorador.

# La prioridad otorgada indica la posicion que debe tener un decorador
# si se combina con otro para una misma funcion.

# Si tiene el mismo nivel de prioridad, entonces no importa el orden en
# que se coloquen entre ellos de mismo nivel.

# Los niveles se toman como 1 para el mas cercano a la funcion y 3 para
# el mas alejado.

# Test:

@timeSleep(2, True)		# Prioridad: 3 (Recomendable que sea el ultimo)
@debug					# Prioridad: 2
@counter				# Prioridad: 2
@timer					# Prioridad: 2
@symbolsTable			# Prioridad: 2
@lowerCase				# Prioridad: 1 (Recomendable que sea el primero)
def test(times, val, xD):
	for _ in range(times):
		s = sum([i**2 for i in range(val)])
	return xD

#=======================================================================



if __name__ == '__main__':
	
	test(12, 12345, (['AB', (5,('fOfo')), {'noO':{'jo12Sd':('JO1')}}, ['Hola', 55]],0))

