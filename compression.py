import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from compression_algorithms import (
    RunLengthEncoding,
    HuffmanEncoding,
    ArithmeticEncoding,
    GolombEncoding,
    LZWEncoding,
    calculate_entropy,
    calculate_probability
)

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lossless Compression Techniques")
        
        self.text_input = tk.scrolledtext.ScrolledText(self.root, width=60, height=10)
        self.text_input.pack(pady=10)
        
        self.m_label = tk.Label(self.root, text="Value of m for Golomb Encoding:")
        self.m_label.pack()
        
        self.m_entry = tk.Entry(self.root)
        self.m_entry.pack()
        
        self.compress_button = tk.Button(self.root, text="Compress", command=self.compress)
        self.compress_button.pack()
        
        self.results_label = tk.Label(self.root, text="Results:")
        self.results_label.pack()
        
        self.results_text = tk.scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.results_text.pack(pady=10)
        
    def compress(self):
        input_text = self.text_input.get("1.0", tk.END).strip()
        
        results = ""
        compression_ratios = {}

        # Calculate and display other metrics
        try:
            entropy = calculate_entropy(input_text)
            probabilities = calculate_probability(input_text)
            results += "Entropy: {:.2f}\n\n".format(entropy)
            results += "Probabilities of occurrence for each character:\n"
            for char, prob in probabilities.items():
                results += f"{char}: {prob:.4f}\n"
            results += "\n"
        except Exception as e:
            messagebox.showerror("Error", f"Error in calculating additional metrics: {e}")
        
        # Run-length encoding
        try:
            rle_ratio, rle_before, rle_value, rle_after, rle_average_length, rle_efficiency = RunLengthEncoding.encode(input_text)
            compression_ratios['Run-Length Encoding'] = rle_ratio
            results += f"Run-Length Encoding:\nBefore: {rle_before} bits\nCode: {rle_value} \nAfter: {rle_after} bits\nAverage Length: {rle_average_length} \nCompression Ratio: {rle_ratio:.2f}\nEfficiency: {rle_efficiency} %\n\n"
        except Exception as e:
            messagebox.showerror("Error in Run-Length Encoding", f"{e}")
        
        # Huffman encoding
        try:
            if isinstance(input_text, int) or input_text.isdigit():  # Check if input_text is an integer or a string representation of an integer
                messagebox.showerror("Error in Huffman Encoding", "Please provide a string.")
            else:
                huffman_ratio, huffman_before, huffman_code, huffman_after, huffman_average_length, huffman_efficiency = HuffmanEncoding.encode(input_text)
                compression_ratios['Huffman Encoding'] = huffman_ratio
                results += f"Huffman Encoding:\nBefore: {huffman_before} bits\nCodeword: {huffman_code} \nAfter: {huffman_after} bits\nAverage Length: {huffman_average_length} \nCompression Ratio: {huffman_ratio:.2f}\nEfficiency: {huffman_efficiency} %\n\n"
        except Exception as e:
            messagebox.showerror("Error in Huffman Encoding", f"{e}")
        
        # Arithmetic encoding
        try:
            arithmetic_ratio, arithmetic_before, arithmetic_value, arithmetic_after,  arithmetic_probabilities, arithmetic_average_length, arithmetic_efficiency = ArithmeticEncoding.arithmetic_encode(input_text)
            compression_ratios['Arithmetic Encoding'] = arithmetic_ratio
            results += f"Arithmetic Encoding:\nBefore: {arithmetic_before} bits\nTag/Code: {arithmetic_value} \nAfter: {arithmetic_after} \nAverage length: {arithmetic_average_length} \nCompression Ratio: {arithmetic_ratio:.2f}\nEfficiency: {arithmetic_efficiency} %\n"
            results += "Probabilities:\n"
            for symbol, prob_range in arithmetic_probabilities.items():
                results += f"{symbol}: {prob_range}\n"
            # Add extra newlines after all probabilities
            results += "\n"
        except Exception as e:
            messagebox.showerror("Error in Arithmetic Encoding", f"{e}")
        
        # Golomb encoding
        try:
            m = int(self.m_entry.get())  # Get the value of m from the entry widget as an integer
            if isinstance(input_text, int):  # Check if input_text is an integer
                golomb_ratio, golomb_before, golomb_value, golomb_after, golomb_average_length, golomb_efficiency = GolombEncoding.golomb_rice_encode(input_text, m)
                compression_ratios['Golomb Encoding'] = golomb_ratio
                results += f"Golomb Encoding:\nBefore: {golomb_before} bits\nCodeword: {golomb_value} \nAfter: {golomb_after} bits\nAverage Length: {golomb_average_length} \nCompression Ratio: {golomb_ratio:.2f} \nEfficiency: {golomb_efficiency} %\n\n"
            elif input_text.isdigit():  # Check if input_text is a digit (string representation of an integer)
                golomb_ratio, golomb_before, golomb_value, golomb_after, golomb_average_length, golomb_efficiency = GolombEncoding.golomb_rice_encode(int(input_text), m)
                compression_ratios['Golomb Encoding'] = golomb_ratio
                results += f"Golomb Encoding:\nBefore: {golomb_before} bits\nCodeword: {golomb_value} \nAfter: {golomb_after} bits\nAverage Length: {golomb_average_length} \nCompression Ratio: {golomb_ratio:.2f} \nEfficiency: {golomb_efficiency} %\n\n"
            else:  # If input_text is not an integer or a string representation of an integer
                messagebox.showerror("Error in Golomb Encoding", "Please provide an integer input.")
        except Exception as e:
            messagebox.showerror("Error in Golomb Encoding", f"{e}")
        
        # LZW encoding
        try:
            lzw_ratio, lzw_before, lzw_value, lzw_after, lzw_average_length, lzw_efficiency = LZWEncoding.lzw_encode(input_text)
            compression_ratios['LZW Encoding'] = lzw_ratio
            results += f"LZW Encoding:\nBefore: {lzw_before} bits\nSequence: {lzw_value} \nAfter: {lzw_after} bits\nAverage Length: {lzw_average_length} \nCompression Ratio: {lzw_ratio:.2f} \nEfficiency: {lzw_efficiency} %\n\n"
        except Exception as e:
            messagebox.showerror("Error in LZW Encoding", f"{e}")
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, results)

        # Display compression ratios
        best_ratios = [key for key, value in compression_ratios.items() if value == max(compression_ratios.values())]
        results += "Compression Ratios:\n"
        for algo, ratio in compression_ratios.items():
            results += f"{algo}: {ratio:.2f}\n"
        results += f"\nBest Compression Algorithm(s): {', '.join(best_ratios)}\n"
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, results)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()
