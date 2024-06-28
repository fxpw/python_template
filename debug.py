class debug:
	# Декоратор для вывода информации о вызове функции
	def print(func):
		def wrapper(*args, **kwargs):
			print(f"TRACE: calling {func.__name__}() with {args}, {kwargs}")
			original_result = func(*args, **kwargs)
			print(f"TRACE: {func.__name__}() returned {original_result!r}")
			return original_result

		return wrapper

	# Декоратор для измерения времени выполнения функции
	def timing(func):
		import time

		def wrapper(*args, **kwargs):
			start = time.time()
			result = func(*args, **kwargs)
			end = time.time()
			print(f"Timing: {func.__name__} took {end - start} seconds to complete")
			return result

		return wrapper

	# Декоратор для перехвата исключений
	def catch_exception(func):
		def wrapper(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except Exception as e:
				print(f"Exception caught in {func.__name__}: {e}")

		return wrapper

	# Декоратор для отделения функций
	def divorce(func):
		def new_func():
			print("*" * 10)
			func()
			print("*" * 10)

		return new_func

	# Декоратор для кэширования результатов функции
	def cache(func):
		memo = {}

		def wrapper(*args, **kwargs):
			if args in memo:
				print(f"Cache hit for {func.__name__} with args {args}")
				return memo[args]
			else:
				result = func(*args, **kwargs)
				memo[args] = result
				return result

		return wrapper

	# Декоратор для проверки типов входных аргументов
	# @debug.type_check((int, int))  # Ожидаем, что оба аргумента будут целыми числами
	def type_check(correct_types):
		def decorator(func):
			def wrapper(*args, **kwargs):
				if len(args) != len(correct_types):
					raise ValueError("Incorrect number of arguments")
				for a, c in zip(args, correct_types):
					if not isinstance(a, c):
						raise TypeError(f"Argument {a} is not of type {c}")
				return func(*args, **kwargs)

			return wrapper

		return decorator

	# Декоратор для логирования уровня вложенности вызовов
	call_depth = 0

	def log_depth(func):
		def wrapper(*args, **kwargs):
			debug.call_depth += 1
			print(f"{'  ' * debug.call_depth}Entering {func.__name__}")
			result = func(*args, **kwargs)
			print(f"{'  ' * debug.call_depth}Exiting {func.__name__}")
			debug.call_depth -= 1
			return result

		return wrapper

	# Декоратор для ограничения времени выполнения функции
	# @debug.timeout(5)  # Ограничение времени выполнения функции до 5 секунд
	def timeout(limit):
		import threading

		def decorator(func):
			def wrapper(*args, **kwargs):
				def interrupt():
					threading.Timer(limit, raise_timeout).start()

				def raise_timeout():
					raise TimeoutError(
						f"Function {func.__name__} exceeded time limit of {limit} seconds"
					)

				interrupt()
				return func(*args, **kwargs)

			return wrapper

		return decorator

	# Декоратор для логирования истории вызовов функции
	call_history = {}

	def log_history(func):
		def wrapper(*args, **kwargs):
			if func.__name__ not in debug.call_history:
				debug.call_history[func.__name__] = []
			debug.call_history[func.__name__].append((args, kwargs))
			result = func(*args, **kwargs)
			return result

		return wrapper

	# Метод для вывода истории вызовов
	@staticmethod
	def print_call_history():
		for func_name, calls in debug.call_history.items():
			print(f"History for {func_name}:")
			for i, call in enumerate(calls, 1):
				args, kwargs = call
				print(f"  {i}. Args: {args}, Kwargs: {kwargs}")

	# Декоратор для автоматического повторения вызова в случае исключений
	# @debug.retry_on_exception(retry_count=3, allowed_exceptions=(ValueError,))
	def retry_on_exception(retry_count=3, allowed_exceptions=(Exception,)):
		def decorator(func):
			def wrapper(*args, **kwargs):
				for _ in range(retry_count):
					try:
						return func(*args, **kwargs)
					except allowed_exceptions as e:
						print(f"Exception caught in {func.__name__}: {e}, retrying...")
				raise

			return wrapper

		return decorator

	# Декоратор для выполнения функции только при выполнении условия
	def if_condition(condition):
		def decorator(func):
			def wrapper(*args, **kwargs):
				if condition():
					return func(*args, **kwargs)
				else:
					print(
						f"Condition for {func.__name__} is not met. Function not executed."
					)

			return wrapper

		return decorator
