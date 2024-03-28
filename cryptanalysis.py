import cipher
from collections import Counter
import matplotlib.pyplot as plt


# Функция для подсчета частоты появления каждой буквы в тексте.
def frequency_analysis(text):
    frequencies = {}
    for char in text:
        if char.isalpha():
            char = char.lower()
            frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


# Поиск ключа для шифра Цезаря
def find_key_caesar(frequencies):
    most_common_letter = max(frequencies, key=frequencies.get)
    shift = ord('о') - ord(most_common_letter)
    return abs(shift)


# Вычисление индекса совпадений
def get_index_of_coincidence(text):
    total = len(text)
    frequency = Counter(text)
    ic = sum(n*(n-1) for n in frequency.values()) / (total * (total - 1))
    return ic


# Поиск длины ключа для шифра Виженера
def get_vigenere_key_length(ciphertext, max_key_length=20):
    average_ic = []  # Список для хранения средних индексов совпадений для различных длин ключа
    for key_length in range(1, max_key_length + 1):
        groups = ['' for _ in range(key_length)]  # Разделяем текст на группы по длине ключа
        for i, char in enumerate(ciphertext):
            groups[i % key_length] += char
        indices_of_coincidence = [get_index_of_coincidence(group) for group in groups]  # Вычисляем индексы совпадений для каждой группы
        average_ic.append(sum(indices_of_coincidence) / len(indices_of_coincidence))  # Усредняем индексы совпадений
    for ic in average_ic:
        if ic > 0.05:
            return average_ic.index(ic) + 1 # Определяем длину ключа как индекс с первым наибольшим значением индекса совпадений


# Подсчет значения хи-квадрата
def chi_squared_score(text):
    # Частоты букв в русском языке
    expected_frequencies = {' ': 0.175, 'о': 0.090, 'е': 0.072, 'ё': 0.072, 'а': 0.062, 'и': 0.062,
    'т': 0.053, 'н': 0.053, 'с': 0.045, 'р': 0.040, 'в': 0.038,
    'л': 0.035, 'к': 0.028, 'м': 0.026, 'д': 0.025, 'п': 0.023,
    'у': 0.021, 'я': 0.018, 'ы': 0.016, 'з': 0.016, 'ь': 0.014,
    'ъ': 0.014, 'б': 0.014, 'г': 0.013, 'ч': 0.012, 'й': 0.010,
    'х': 0.009, 'ж': 0.007, 'ю': 0.006, 'ш': 0.006, 'ц': 0.004,
    'щ': 0.003, 'э': 0.003, 'ф': 0.002}

    # Подсчет частот букв в тексте
    text_length = len(text)
    # Количество букв тексте
    letter_frequencies = Counter(text.lower())
    # Ожидаемое количество букв в тексте
    expected_letter_frequencies = {letter: text_length * expected_frequencies[letter] for letter in letter_frequencies}
    # Вычисление значения критерия хи-квадрат
    chi_squared = sum((letter_frequencies[char] - expected_letter_frequencies[char]) ** 2 / expected_letter_frequencies[char]
                      for char in letter_frequencies)
    return chi_squared


# Поиск ключа Виженера
def find_vigenere_key(ciphertext, key_length):
    possible_key = ''
    # Разбиение зашифрованного текста на блоки
    blocks = [ciphertext[i::key_length] for i in range(key_length)]
    # Поиск символов ключа для каждой позиции
    alphabet ='абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for block in blocks:
        score = []
        # Попробуем каждую букву в алфавите
        for char in alphabet:
            # Расшифровываем блок
            decrypted_block = ''.join(chr(abs((ord(c) - ord('а')) - (ord(char) - ord('а'))) % 32 + ord('а')) for c in block)
            # Оцениваем степень схожести с русским языком с помощью критерия хи-квадрат
            score.append(chi_squared_score(decrypted_block))
        # Обновляем ключ
        possible_key += alphabet[score.index(min(score))]
    return possible_key


# Построение алфавита замены
def build_substitution_alphabet(keyword):
    # Создаем пустой алфавит замены
    substitution_alphabet = {}

    # Строим алфавит замены
    for i, char in enumerate(keyword):
        alphabet = [chr((j - ord('а') + ord(char)) % 32 + ord('а')) for j in range(32)]
        substitution_alphabet[char] = alphabet

    return substitution_alphabet


# Расшифровка шифра Виженера
def decrypt_vigenere(ciphertext, keyword):
    substitution_alphabet = build_substitution_alphabet(keyword)
    plaintext = ''
    keyword_length = len(keyword)
    keyword_index = 0  # Индекс для символов ключевого слова

    # Дешифруем текст с помощью квадрата виженера
    for char in ciphertext:
        keyword_char = keyword[keyword_index % keyword_length]
        vigenere_column = substitution_alphabet[keyword_char]
        vigenere_row_index = vigenere_column.index(char)
        plaintext += chr(ord('а') + vigenere_row_index)
        keyword_index += 1

    return plaintext

#
def calculate_letter_frequencies(text):
    # Приводим текст к нижнему регистру
    text = text.lower()
    # Удаляем все символы, кроме букв
    text = ''.join(filter(str.isalpha, text))
    # Подсчитываем частоту каждой буквы
    letter_counts = Counter(text)
    # Сортируем буквы по частоте
    sorted_letter_counts = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_letter_counts

def calculate_bigram_frequencies(text):
    # Приводим текст к нижнему регистру
    text = text.lower()
    # Удаляем все символы, кроме букв
    text = ''.join(filter(str.isalpha, text))
    # Создаем список биграмм
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    # Подсчитываем частоту каждой биграммы
    bigram_counts = Counter(bigrams)
    # Сортируем биграммы по частоте
    sorted_bigram_counts = sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_bigram_counts

def plot_histogram(data, title):
    labels, values = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel('Буква или биграмма')
    plt.ylabel('Частота')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    mode = input("Выберите режим (1 - Цезарь, 2 - Виженер): ")
    if mode == "1":
        # Вычисление частоты встречающихся символов и нахождение ключа
        with open("encC_text.txt", "r", encoding="utf-8") as file:
            encrypted_text_caesar = file.read()

        frequencies_caesar = frequency_analysis(encrypted_text_caesar)
        key_caesar = find_key_caesar(frequencies_caesar)

        # Расшифровка
        decrypted_text_caesar = cipher.caesar_decrypt(encrypted_text_caesar, key_caesar)
        with open("decC_text.txt", "w", encoding='utf-8') as file:
            file.write(decrypted_text_caesar)

        # Вывод первых строк файлов
        with open("encC_text.txt", "r", encoding='utf-8') as file:
            print("Содержимое файла encC_text.txt:")
            print(file.readline().strip())

        with open("decC_text.txt", "r", encoding='utf-8') as file:
            print("Содержимое файла decC_text.txt:")
            print(file.readline().strip())
    if mode == "2":
        # Вычисление частоты встречающихся символов и нахождение ключа
        with open("encV_text.txt", "r", encoding="utf-8") as file:
            encrypted_text_vigenere = file.read()

        # Удаление символов, чтобы остались только буквы
        encrypted_text_vigenere = ''.join(filter(lambda x: x not in ' ,.;!?:()-«»—', encrypted_text_vigenere.lower()))
        encrypted_text_vigenere = encrypted_text_vigenere.replace("'", "")
        encrypted_text_vigenere = encrypted_text_vigenere.replace("\n", "")
        encrypted_text_vigenere = encrypted_text_vigenere.replace("...", "")

        key_length = get_vigenere_key_length(encrypted_text_vigenere)

        keyword = find_vigenere_key(encrypted_text_vigenere, key_length)
        print(keyword)

        substitution_alphabet = build_substitution_alphabet(keyword)
        # Выводим алфавит замены
        for key, value in substitution_alphabet.items():
            print(f"{key}: {' '.join(value)}")

        # Расшифровка
        plain_text = decrypt_vigenere(encrypted_text_vigenere, keyword)
        print(plain_text)

        #################### Частотный анализ ####################
        with open("text_expand.txt", "r", encoding="utf-8") as file:
            text = file.read()
        # Подсчет частот букв
        letter_frequencies = calculate_letter_frequencies(text)
        # Построение диаграммы для 10 наиболее часто встречающихся букв
        plot_histogram(letter_frequencies[:10], 'Частота букв')
        # Подсчет частот биграмм
        bigram_frequencies = calculate_bigram_frequencies(text)
        # Построение диаграммы для 10 наиболее часто встречающихся биграмм
        plot_histogram(bigram_frequencies[:10], 'Частота биграмм')


if __name__ == "__main__":
    main()
