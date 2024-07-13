import heapq
from collections import Counter
import math

class RunLengthEncoding:
    @staticmethod
    def encode(data):
        if isinstance(data, int):  # If input is an integer, convert it to binary string
            binary_text = bin(data)[2:]
            return binary_text, len(binary_text) / 8  # Assuming 1 byte per character for simplicity

        encoded_text = ""
        count = 1
        max_count = 1  # Initialize max_count
        num_vectors = 0  # Initialize the number of vectors
        
        for i in range(1, len(data)):
            if data[i] == data[i - 1]:
                count += 1
                if count > max_count:  # Update max_count if needed
                    max_count = count
            else:
                encoded_text += data[i - 1] + str(count)  # Ensure each count is represented in 8 bits
                count = 1
                num_vectors += 1  # Increment the number of vectors when the character changes
        
        encoded_text += data[-1] + str(count)  # Ensure the last count is represented in 8 bits
        num_vectors += 1  # Increment the number of vectors for the last character sequence
        
        encoded_length = num_vectors * (8 + math.ceil(math.log2(max_count + 1)))  # Total bits used in the encoded text
        
        original_length = len(data) * 8  # Total bits in the original uncompressed data
        ratio = original_length / encoded_length  # Calculate the compression ratio
        average_length = encoded_length / len(data)  # Calculate the average length encoding
        entropy = calculate_entropy(data)
        efficiency = (entropy / average_length) * 100
        return ratio, original_length, encoded_text, encoded_length, average_length, efficiency

class HuffmanEncoding:
    class HuffmanNode:
        def __init__(self, char, frequency):
            self.char = char
            self.frequency = frequency
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.frequency < other.frequency

    @staticmethod
    def build_tree(data):
        if isinstance(data, int):  # If input is an integer, convert it to binary string
            binary_text = bin(data)[2:]
            return binary_text, len(binary_text) / 8  # Assuming 1 byte per character for simplicity

        frequency = Counter(data)
        heap = [HuffmanEncoding.HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanEncoding.HuffmanNode(None, left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        return heap[0]

    @staticmethod
    def build_codewords(node, current_code, codewords):
        if node.char is not None:
            codewords[node.char] = current_code
        else:
            HuffmanEncoding.build_codewords(node.left, current_code + "0", codewords)
            HuffmanEncoding.build_codewords(node.right, current_code + "1", codewords)

    @staticmethod
    def encode(data):
        if isinstance(data, int):  # If input is an integer, convert it to binary string
            binary_text = bin(data)[2:]
            return binary_text, len(binary_text) / 8  # Assuming 1 byte per character for simplicity

        root = HuffmanEncoding.build_tree(data)
        codewords = {}
        frequency = Counter(data)
        HuffmanEncoding.build_codewords(root, "", codewords)
        original_length = len(data) * 8  # Total bits in the original uncompressed data
        encoded_text = "".join(codewords[char] for char in data)
        encoded_length = len(encoded_text)
        ratio = original_length / encoded_length
        average_length = sum(len(codewords[char]) * freq for char, freq in frequency.items()) / len(data)
        entropy = calculate_entropy(data)
        efficiency = (entropy / average_length) * 100
        return ratio, original_length, encoded_text, encoded_length, average_length, efficiency

class ArithmeticEncoding:
    @staticmethod
    def calculate_probabilities(text):
        # Count the frequency of each symbol in the text
        symbol_counts = Counter(text)
        
        # Calculate probabilities based on symbol counts
        total_symbols = len(text)
        probabilities = {symbol: (0, count / total_symbols) for symbol, count in symbol_counts.items()}
        
        # Update the upper bounds of probabilities
        cumulative_prob = 0
        for symbol in sorted(probabilities):
            probabilities[symbol] = (cumulative_prob, cumulative_prob + probabilities[symbol][1])
            cumulative_prob = probabilities[symbol][1]
        
        return probabilities

    @staticmethod
    def arithmetic_encode(text):
        # Calculate probabilities from the text
        probabilities = ArithmeticEncoding.calculate_probabilities(text)

        # Initialize the range
        low = 0.0
        high = 1.0

        # Encode each symbol in the text
        encoded_length = 0  # Initialize encoded length counter
        for symbol in text:
            # Update the range based on the probabilities
            symbol_range = high - low
            high = low + symbol_range * probabilities[symbol][1]
            low = low + symbol_range * probabilities[symbol][0]

            # Count the number of bits needed to represent the range
            range_bits = -math.floor(math.log2(symbol_range))

            # Update the encoded length
            encoded_length += range_bits

        # Return the mean of the range as the encoded value
        original_length = len(text) * 8  # Total bits in the original uncompressed data
        encoded_value = (low + high) / 2
        ratio = original_length / encoded_length  # Calculate the compression ratio
        # Convert the encoded value to bits
        average_length = encoded_length / len(text)  # Average length per symbol
        entropy = calculate_entropy(text)
        efficiency = entropy / average_length * 100
        return ratio, original_length, encoded_value, encoded_length, probabilities, average_length, efficiency

    @staticmethod
    def arithmetic_decode(encoded_value, length, probabilities):
        decoded_word = []
        for _ in range(length):
            for symbol, prob_range in probabilities.items():
                if prob_range[0] <= encoded_value < prob_range[1]:
                    decoded_word.append(symbol)
                    encoded_value = (encoded_value - prob_range[0]) / (prob_range[1] - prob_range[0])
                    break
        return ''.join(decoded_word)

class GolombEncoding:

    @staticmethod
    def golomb_rice_encode(value, M):
        quotient = value // M
        remainder = value % M

        # Encode quotient in unary; a sequence of 1s followed by a 0.
        unary = '1' * quotient + '0'

        # Encode remainder in binary. The length of the binary representation is log2(M).
        binary_length = M.bit_length() - 1
        binary = format(remainder, f'0{binary_length}b')

        original_length = len(str(value)) * 8  # Total bits in the original uncompressed data
        encoded_value = unary + binary
        encoded_length = len(encoded_value)
        ratio = original_length / encoded_length  # Calculate the compression ratio
        average_length = encoded_length / len(str(value))
        entropy = calculate_entropy(value)
        efficiency = entropy / average_length * 100

        return ratio, original_length, encoded_value, encoded_length, average_length, efficiency

    @staticmethod
    def golomb_rice_decode(encoded, M):
        # Split the encoded string into unary (quotient) and binary (remainder) parts.
        quotient = 0
        while encoded[quotient] == '1':
            quotient += 1
        encoded = encoded[quotient + 1:]  # Skip over the unary part and the separator '0'.

        binary_length = M.bit_length() - 1
        remainder = int(encoded[:binary_length], 2)

        value = quotient * M + remainder

        return value


class LZWEncoding:
    @staticmethod
    def lzw_encode(data):
        dictionary = {chr(i): i for i in range(128)}
        result = []
        w = ""
        
        for c in data:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = len(dictionary)
                w = c
        
        if w:
            result.append(dictionary[w])
        
        original_length = len(data) * 8  # Total bits in the original uncompressed data
        encoded_value = result
        encoded_length = len(result) * 8
        ratio = original_length / encoded_length  # Calculate the compression ratio
        average_length = sum(len(bin(val)[2:]) for val in result) / len(data)
        entropy = calculate_entropy(data)
        efficiency = (entropy / average_length) * 100

        return ratio, original_length, encoded_value, encoded_length, average_length, efficiency

def calculate_entropy(text):
    probabilities = calculate_probability(text)
    entropy = sum(-prob * math.log(prob, 2) for prob in probabilities.values())
    return entropy

def calculate_probability(text):
    if isinstance(text, int):  # Check if text is an integer
        text = str(text)  # Convert integer to string
    probabilities = {}
    total_chars = len(text)
    frequency = Counter(text)
    for char, count in frequency.items():
        probabilities[char] = count / total_chars
    return probabilities
