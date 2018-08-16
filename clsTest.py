from FullTextSum.clsPreprocessDoc import Preprocess

directory_in_str = '/Users/coshiang/Downloads/Dataset/'
text_directory_in_str = '/Users/coshiang/Downloads/Dataset_text/'
import glob
from unidecode import unidecode
file_list = list()

for filename in glob.iglob(directory_in_str + '*.nxml'):
    file_list.append(filename)

pre_precess = Preprocess()
# import os, shutil
# i = 0
for file_path in file_list:
    # i += 1
    # src = file_path
    # dst = file_path.replace('Dataset','Dataset_bioinfo')
    # shutil.move(src, dst)
    #
    # if i == 157:
    #     exit()
    # else:
    #     continue

    dict_paragraphs = pre_precess.read_file(file_path)

    paragraph_list = list()
    conclusion_list = list()

    for paragraph in dict_paragraphs:
        if paragraph['section'] == 'Conclusions':
            conclusion_list.append("".join(i for i in paragraph['text'] if ord(i) < 128))
        else:
            paragraph_list.append("".join(i for i in paragraph['text'] if ord(i) < 128))

    paragraph_list = paragraph_list + conclusion_list

    text_file_path = file_path.replace(directory_in_str,text_directory_in_str)
    text_file_path = text_file_path.replace('.nxml', '.txt')
    print(text_file_path)

    with open(text_file_path, 'w') as f:
        for item in paragraph_list:
            f.write("{}\n".format(item))
