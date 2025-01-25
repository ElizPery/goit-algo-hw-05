import timeit

def measure_time(search_func, main_text, pattern):
    start_time = timeit.default_timer()
    searched_data = search_func(main_text, pattern)
    execution_time = timeit.default_timer() - start_time
    return searched_data, execution_time


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # if no substring is found


def build_shift_table(pattern):
    """Create offset table for Boer-Moore algorithm."""
    table = {}
    length = len(pattern)
    # For each character in the substring, set the offset equal to the length of the substring
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1  
    # If the symbol is not in the table, the offset will be equal to the length of the substring
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    # Create a table of offsets for the pattern (substring)
    shift_table = build_shift_table(pattern)
    i = 0 # Initialize the starting index for the body text

    # We pass through the main text, comparing with the substring
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 # We start from the end of the substring

        # Compare the characters from the end of the substring to its beginning
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 # We shift to the beginning of the substring

        # If the whole substring coincides, return its position in the text
        if j < 0:
            return i # Substring found

        # We shift the index i based on the offset table
        # This allows you to "jump" over mismatched parts of the text
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # If no substring is found, return -1
    return -1
    

def polynomial_hash(s, base=256, modulus=101):
    """
    Returns the polynomial hash of a string s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    # Main row and search substring lengths
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Base number to hash and module
    base = 256 
    modulus = 101  
    
    # Hash value for search substring and current line in main line
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Previous value for hash recalculation
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # We pass through the main line
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        return content
    

main_string_1 = read_file("public1.txt")
substring_1_1 = "алгоритм"
substring_1_2 = "шинапотплгп"

print(f"\nRabin Karp search of the text 1 with the substring that exist: {measure_time(rabin_karp_search, main_string_1, substring_1_1)}")

print(f"Boyer Moore search of the text 1 with the substring that exist: {measure_time(boyer_moore_search, main_string_1, substring_1_1)}")

print(f"Kmp search of the text 1 with the substring that exist: {measure_time(kmp_search, main_string_1, substring_1_1)}")

print(f"\nRabin Karp search of the text 1 with the substring that DOESN'T exist: {measure_time(rabin_karp_search, main_string_1, substring_1_2)}")

print(f"Boyer Moore search of the text 1 with the substring that DOESN'T exist: {measure_time(boyer_moore_search, main_string_1, substring_1_2)}")

print(f"Kmp search of the text 1 with the substring that DOESN'T exist: {measure_time(kmp_search, main_string_1, substring_1_2)}")


main_string_2 = read_file("public2.txt")
substring_2_1 = "баз"
substring_2_2 = "оиненопиьи"

print(f"\nRabin Karp search of the text 2 with the substring that exist: {measure_time(rabin_karp_search, main_string_2, substring_2_1)}")

print(f"Boyer Moore search of the text 2 with the substring that exist: {measure_time(boyer_moore_search, main_string_2, substring_2_1)}")

print(f"Kmp search of the text 2 with the substring that exist: {measure_time(kmp_search, main_string_2, substring_2_1)}")

print(f"\nRabin Karp search of the text 2 with the substring that DOESN'T exist: {measure_time(rabin_karp_search, main_string_2, substring_2_2)}")

print(f"Boyer Moore search of the text 2 with the substring that DOESN'T exist: {measure_time(boyer_moore_search, main_string_2, substring_2_2)}")

print(f"Kmp search of the text 2 with the substring that DOESN'T exist: {measure_time(kmp_search, main_string_2, substring_2_2)}\n")