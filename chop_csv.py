import csv

input_file = "./output_landmarks.csv"
output_file = "./output_landmarks_small.csv"

KEEP_EVERY = 10   # keep every 10th row

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for i, row in enumerate(reader):
        if i % KEEP_EVERY == 0:
            writer.writerow(row)

print("Done! Saved:", output_file)
