import math
from concurrent.futures import ThreadPoolExecutor
import threading

def calculate_term(n, x):
    return ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)

def calculate_term_sum(args):
    start, end, x = args
    return sum(calculate_term(i, x) for i in range(start, end))

def calculate_total_sum(results):
    total_sum = sum(results)
    return total_sum

def main():
    x = float(input("valor x: "))
    term_count = int(input("cant terminos a calcular: "))
    reference_value = float(input("valor referencia: "))

    thread_count = min(term_count, 10)  
    terms_per_thread = term_count // thread_count

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(calculate_term_sum, ((i * terms_per_thread, (i + 1) * terms_per_thread, x) for i in range(thread_count))))

    total_sum = calculate_total_sum(results)

    print("suma total:", total_sum)
    print("diferencia:", total_sum - reference_value)

if __name__ == "__main__":
    main()