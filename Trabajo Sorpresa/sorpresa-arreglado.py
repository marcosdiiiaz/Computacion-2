import threading
import math

def calculate_term(n, x):
    term = ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    return term

def calculate_term_sum(n, x, results, lock):
    term = calculate_term(n, x)
    with lock:
        results.append(term)

def calculate_total_sum(results, lock, total_sum):
    with lock:
        total_sum[0] += sum(results)

def main():
    x = float(input("valor x: "))
    num_terms = int(input("cant de terminos: "))
    reference = float(input("referencia: "))

    results = []
    lock = threading.Lock()
    total_sum = [0]
    term_threads = []

    term_threads = [threading.Thread(target=calculate_term_sum, args=(n, x, results, lock)) for n in range(num_terms)]
    for thread in term_threads:
        thread.start()

    sum_thread = threading.Thread(target=calculate_total_sum, args=(results, lock, total_sum))
    sum_thread.start()

    difference = total_sum[0] - reference

    print("suma total:", total_sum[0])
    print("diferencia:", difference)

if __name__ == "__main__":
    main()