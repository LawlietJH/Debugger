
# Decoradores para depurar funciones.
# Debugger.py
# Python 3
# By: LawlietJH
# - - - v1.2.1


import functools
import time
import sys


#=======================================================================
def timer(func):						# Recibe la Función.
	@functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):			# Recibe los parametros de la funcion.
		
		tmp_ini = time.perf_counter()		# Obtiene el Tiempo actual antes de correr la función.
		valores = func(*args, **kwargs)		# Ejecuta la Función.
		tmp_fin = time.perf_counter()		# Obtiene el Tiempo actual despues de correr la función.
		tmp_tot = tmp_fin - tmp_ini			# Calcula el tiempo transcurrido.
		
		print(f'\n [+] Terminada la función \'{func.__name__}()\' en {tmp_tot:.4f} segundos.\n')
		
		return valores
	return fArgs
#=======================================================================

#=======================================================================
def counter(func):
	"""
	Este es un decorador que cuenta e impríme el número de veces que la función ha sido ejecutada.
	"""
	@functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):
		
		fArgs.count = fArgs.count + 1
		valores = func(*args, **kwargs)
		
		print(f'\n [+] La Función \'{func.__name__}()\' Ha Sido Utilizada {fArgs.count} veces.\n')
		
		return valores
	fArgs.count = 0
	return fArgs
#=======================================================================

#=======================================================================
def debug(func):						# Recibe la Función.
	@functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
	def fArgs(*args, **kwargs):			# Recibe los parametros de la funcion.
		
		rargs   = [repr(a) for a in args]
		rkwargs = [f'{k}={v!r}' for k, v in kwargs.items()]
		rArgs   = ', '.join(rargs + rkwargs)
		
		valores = func(*args, **kwargs)
		
		print(f'\n [+] Función y Parámetros: {func.__name__}({rArgs})\n [+] Devuelve: {valores!r}\n')
		
		return valores
	return fArgs

# Ejemplo de Decorador con Parameros: @debug(params)
# ~ def debug(*args, **kwargs):					# Recibe los parametros del decorador. Obliga a utilizarlo como @debug()
	# ~ def fDebug(func):						# Recibe la Función.
		# ~ @functools.wraps(func)				# Coloca a la Función como principal y no al decorador.
		# ~ def fArgs(*args, **kwargs):			# Recibe los parametros de la funcion.
			# ~ ...
			# ~ valores = func(*args, **kwargs)
			# ~ ...
			# ~ return valores
		# ~ return fArgs
	# ~ return fDebug
#=======================================================================

#=======================================================================
class getSymbolsTable(object):
	
	def __init__(self, func):
		
		self._locals = {}
		self.func = func
	
	def __call__(self, *args, **kwargs):
		
		def tracer(frame, event, arg):
			if event=='return':
				self._locals = frame.f_locals.copy()
		
		sys.setprofile(tracer)
		try: valores = self.func(*args, **kwargs)
		finally: sys.setprofile(None)
		
		self.locals					# Imprime La Tabla de Símbolos de la Función Indicada.
		
		return valores
	
	@property
	def __name__(self):				# Coloca a la Función como principal y no al decorador.
		return self.func.__name__
	
	@property			# permite ejecutar la funcion 'self.locals()' como 'self.locals'.
	def locals(self):
		print(f'\n [+] Tabla de Símbolos en la función \'{self.func.__name__}()\':\n')
		for i, (x, y) in enumerate(self._locals.items()):
			print(f'\t [{i+1}]: {x} = {y}')
		print('')
#=======================================================================



#=======================================================================
# Test:

@debug
@counter
@timer
@getSymbolsTable
def test(times, val):
	for _ in range(times):
		s = sum([i**2 for i in range(val)])
#=======================================================================



if __name__ == '__main__':
	
	test(12, 12345)


