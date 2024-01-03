import os
def replace_first_word(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Modify each line to ensure the first word is '1' or '0' accordingly
    for i, line in enumerate(lines):
        words = line.strip().split()
        if words:
            if words[0] != '1':
                words[0] = '1'
            lines[i] = ' '.join(words) + '\n'

    # Write the updated content back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)


label_dir_test = 'test/labels'
label_dir_train = 'train/labels'
label_dir_valid = 'valid/labels'


# List image files in the directory
label_files_test = os.listdir(label_dir_test)
label_files_train = os.listdir(label_dir_train)
label_files_valid = os.listdir(label_dir_valid)

# Process each image and its corresponding label
for label_file_test in label_files_test:
    image_path = os.path.join(label_dir_test, label_file_test)
    replace_first_word(image_path)

for label_file_train in label_files_train:
    image_path = os.path.join(label_dir_train, label_file_train)
    replace_first_word(image_path)

for label_file_valid in label_files_valid:
    image_path = os.path.join(label_dir_valid, label_file_valid)
    replace_first_word(image_path)


