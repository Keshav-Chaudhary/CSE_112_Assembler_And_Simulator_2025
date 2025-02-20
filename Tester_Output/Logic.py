def compare_files(file1, file2):
    differing_lines = []
    
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line_num, (line1, line2) in enumerate(zip(f1, f2), start=1):
            if line1.strip() != line2.strip():
                print(f"Line {line_num}: {line1.strip()} != {line2.strip()}")

                differing_lines.append(line_num)
    
    return differing_lines

# Example usage:
file1 = "InputFile1.txt"
file2 = "InputFile2.txt"
differences = compare_files(file1, file2)

if differences:
    print("Lines that differ:", differences)
else:
    print("Files are identical.")