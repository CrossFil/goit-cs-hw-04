import os
import random
import threading
import multiprocessing
import time

# 1. Генерация случайного текста для файла texts.txt
def generate_random_text_file(file_path, word_count_min=200, word_count_max=300):
    word_list = [
        "Python", "code", "multiprocessing", "threading", "development", "parallel", 
        "task", "performance", "execution", "function", "process", "thread", "programming", 
        "algorithm", "data", "file", "input", "output", "memory", "disk", "search", "keyword", 
        "result", "error", "exception", "time", "CPU", "core", "IO", "speed", "efficiency", 
        "operation", "system", "concurrency", "lock", "shared", "variable", "array", 
        "list", "dictionary", "queue", "management", "resource", "limit", "computation", 
        "distribution", "application", "problem", "solution", "optimization", "sync", 
        "asynchronous", "blocking", "non-blocking", "context", "switch", "runtime", 
        "compile", "linker", "debugger", "test", "unit", "integration", "system", "monitoring", 
        "threadpool", "scheduler", "resource", "intensive", "lightweight", "overhead", 
        "profiling", "analysis", "statistics", "logging"
    ]

    random_text = " ".join(random.choices(word_list, k=random.randint(word_count_min, word_count_max)))
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(random_text)

    print(f"File {file_path} successfully created with random words.")


# 2. Многопоточная версия программы
def search_keywords_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def thread_search(files, keywords):
    results = {keyword: [] for keyword in keywords}
    threads = []
    
    for file_path in files:
        thread = threading.Thread(target=search_keywords_in_file, args=(file_path, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return results

def main_threading(file_directory, keywords):
    start_time = time.time()
    
    files = [os.path.join(file_directory, file) for file in os.listdir(file_directory) if file.endswith('.txt')]
    results = thread_search(files, keywords)
    
    end_time = time.time()
    print(f"Threading version completed in {end_time - start_time:.2f} seconds.")
    
    return results


# 3. Многопроцессорная версия программы
def search_keywords_in_file_multiprocessing(file_path, keywords, queue):
    result = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    result[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    queue.put(result)

def process_search(files, keywords):
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    processes = []

    for file_path in files:
        process = multiprocessing.Process(target=search_keywords_in_file_multiprocessing, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword in keywords:
            final_results[keyword].extend(result[keyword])

    return final_results

def main_multiprocessing(file_directory, keywords):
    start_time = time.time()
    
    files = [os.path.join(file_directory, file) for file in os.listdir(file_directory) if file.endswith('.txt')]
    results = process_search(files, keywords)
    
    end_time = time.time()
    print(f"Multiprocessing version completed in {end_time - start_time:.2f} seconds.")
    
    return results


# 4. Основная программа, которая объединяет все
if __name__ == "__main__":
    keywords = ["Python", "code", "multiprocessing", "threading"]
    file_directory = "./"  # Папка, где будет храниться текстовый файл

    # Генерация файла texts.txt
    text_file_path = os.path.join(file_directory, "texts.txt")
    generate_random_text_file(text_file_path)

    # Запуск многопоточной версии
    print("\nRunning threading version:")
    thread_results = main_threading(file_directory, keywords)
    print("Threading results:", thread_results)

    # Запуск многопроцессорной версии
    print("\nRunning multiprocessing version:")
    process_results = main_multiprocessing(file_directory, keywords)
    print("Multiprocessing results:", process_results)
