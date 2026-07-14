print("\n========================================================")
print("| codePlagiarismCheck: Python Codes Similarity Checker |")
print("========================================================")

# set the variable folder_name to the name of the folder accordingly
# this check.py code must be in the same parent directory as the folder
folder_name = input("Input the directory (folder) name : ")

import time
start = time.time()
import difflib  # difference library
import ast  # Abstract Syntax Tree (AST)
import os
import csv

# token-based similarity comparison
def token_based_similarity(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()
    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
    return similarity

# AST-based similarity comparison
def ast_based_comparison(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        tree1 = ast.parse(f1.read())
        tree2 = ast.parse(f2.read())
    return ast.dump(tree1) == ast.dump(tree2)

# double comparison
def compare_files(file1, file2):
    token_similarity = token_based_similarity(file1, file2)
    ast_similarity = ast_based_comparison(file1, file2)
    return token_similarity, ast_similarity

# criterion for token-based similarity test
plagiarize_value = 0.75
warning_value = 0.50

# batch comparison of all files in a directory
def batch_compare(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.py')]
    global file_count
    file_count = len(files)
    print(f"Number of .py files in '{directory}': {file_count}\n")
    results = []

    # comparison of each files
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[j])
            token_sim, ast_sim = compare_files(file1, file2)
            if token_sim >= plagiarize_value:
                exceeds_threshold = "PLAGIARIZED"
            elif token_sim >= warning_value and token_sim < plagiarize_value:
                exceeds_threshold = "WARNING"
            else:
                exceeds_threshold = "OK"
            results.append\
            ({
                'file1': files[i],
                'file2': files[j],
                'token_similarity': token_sim,
                'ast_similarity': ast_sim,
                'status': exceeds_threshold
            })

            print(f"Compared {files[i]} and {files[j]} - "
                  f"Token similarity: {token_sim:.2f}, AST similarity: {ast_sim}, Status: {exceeds_threshold}")

    return results

# execution
directory_path = f'{folder_name}'
print(f"\nComparing files in {folder_name} directory...")
results = batch_compare(directory_path)
print("\nComparison Finished.")
print(f"Number of .py files in '{directory_path}': {file_count}\n")

# save
results_file = f'results_{directory_path.strip("/")}.csv'
with open(results_file, 'w', newline='') as csvfile:
    fieldnames = ['file1', 'file2', 'token_similarity', 'ast_similarity', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow(result)

end = time.time()
print(f"Execution Time = {round(end-start,3)} s")
print(f"Comparison complete! Results saved to {results_file}.\n")
