#importing the regex module
import re,os
from difflib import get_close_matches
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image
import shutil

#user defined input
directory = input("Enter target directory:")
result_directory = input("Enter result folder destination:")

# create result directories
result_dir = os.path.join(result_directory,'results')
file_type_list_dir = os.path.join(result_directory,'results','file_type_lists')
filename_word_match_list_dir = os.path.join(result_directory,'results','filename_word_match_lists')
wordsearch_file_list_dir = os.path.join(result_directory,'results','wordsearch_file_lists')
word_matched_image_list_dir = os.path.join(result_directory,'results','word_matched_image_lists')
other_image_list_dir = os.path.join(result_directory,'results','other_image_lists')

try:
	os.mkdir(file_type_list_dir,mode=755)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('Directory already exists')
    else:
        raise

try:
	os.mkdir(filename_word_match_list_dir,mode=755)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('Directory already exists')
    else:
        raise

try:
	os.mkdir(wordsearch_file_list_dir,mode=755)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('Directory already exists')
    else:
        raise
		
try:
	os.mkdir(word_matched_image_list_dir,mode=755)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('Directory already exists')
    else:
        raise

try:
	os.mkdir(other_image_list_dir,mode=755)
except OSError as e:
    if e.errno == errno.EEXIST:
        print('Directory already exists')
    else:
        raise
						
# dictionaries to keep for analysis
word_counts = {}
file_type_catelog = {}
word_matched_image_files = {}
other_image_files = {}
word_matched_filenames = {}
word_matched_files = {}
word_substitutions = {}

# important predefined lists
image_file_types = [".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp",".png",".gif",".apng",".avif",".svg",".webp",".bmp",".ico", ".cur",".tif", ".tiff"]

def find_image_filepath():
	file = None
	filepath = None
	file = filedialog.askopenfile(mode='r', filetypes=[('Image Files', image_file_types)])
	if file:
		filepath = os.path.abspath(file.name)
	return filepath

def open_image(filepath):
	# open method used to open different extension image file
	im = Image.open(filepath) 
	# show image
	im.show()

def replace_images(dictionary):
	for k in dictionary.keys():
		print(k + " file type")
		for original_filepath in dictionary[k]:
			ask_again = True
			while ask_again:
				print("Original Image:")
				print(original_filepath)
				open_image(original_filepath)
				replace_q = input("Want to replace this?").lower()
				if replace_q.startswith("y"):
					new_image_filepath = find_image_filepath()
					if new_image_filepath:
						print("Replace With")
						print(new_image_filepath)
						open_image(new_image_filepath)
						confirm_q = input("Replace with this?").lower()
						if confirm_q.startswith("y"):
							shutil.move(new_image_filepath,original_filepath)
							print("done")
							ask_again = False
						else:
							print("Let's try again...")
				else:
					ask_again = False
	print("Those are all the images")
	return
			

#defining the replace method
def replace_words_in_file(filePath, text, subs, flags=0):
    with open(file_path, "r+") as file:
        #read the file contents
        file_contents = file.read()
        text_pattern = re.compile(re.escape(text), flags)
        file_contents = text_pattern.sub(subs, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)

def replace_words_in_string(original_str,text, subs, flags=0):
	text_pattern = re.compile(re.escape(text), flags)
    new_string = text_pattern.sub(subs, original_str)
	return new_string


def match_filenames(file_list, list_of_words):
	returning_dictionary = {}
	for x in list_of_words:
		li = [y for y in get_close_matches(x,sp,n=1000000000,cutoff=0.1) if x in y]
		if len(li)>0:
			returning_dictionary[x] = li 		
	return returning_dictionary

def wordsearch_dict_filename_lists():
	# create nested dictionary
	for k in file_type_catelog.keys():
		# go thru imagery filename dictionary to check for matching
		if k in image_file_types:
			matched_dict = match_filenames(file_type_catelog[k],list_of_words)
			if len(matched_dict)>0:
				word_matched_image_files[k] = matched_dict
			else:
				other_image_files[k] = matched_dict
		# if not image file, catelog other files
		else:
			matched_dict = match_filenames(file_type_catelog[k],list_of_words)
			if len(matched_dict)>0:
				word_matched_filenames[k] = matched_dict
	return
	
def wordsearch_file(filename,list_of_words):	
	with open(filename) as df:
		data = df.read()
		sp = data.split()
		for x in list_of_words:
			li = [y for y in get_close_matches(x,sp,cutoff=0.5) if x in y]
				word_counts[nw] = counts.get(nw, 0) + 1
			#check if filename for new word (nw) is recorded,add if not
			for nw in li:
				if nw in word_matched_files.keys():
					if filename not in word_matched_files[nw]:
						word_matched_files[nw].append(filepath)	
	return
	
def catelog_files(directory):
	print('Cateloging Files...')
	for root, dirs, files in os.walk(directory):
		for filename in files:
			filepath = os.path.join(path,filename)
			# catelog file types
			extension = filename.split(".")[-1]
			if extension not in file_type_catelog.keys():
				file_type_catelog[extension] = []
			file_type_catelog[extension].append(filepath)
	print("Files Cateloged:")
	for k in file_type_catelog.keys():
		print('    %-7s %d' %(k,len(file_type_catelog[k])))
	return

def save_dict_values_by_keys(dictionary,destination_dir):
	for k in dictionary.keys():
		txtfile = open(os.path.join(destination_dir,k + '.txt'),'w')
		for e in dictionary[k]:
			txtfile.write(e + "\n")
		txtfile.close()

def search_files_word_matches():
	for k in file_type_catelog.keys():
		# go thru filename dictionary to check for matching words inside files
		if k not in image_file_types:
			for f in file_type_catelog[k]:
				wordsearch_file(filename,list_of_words)
	return

def wordsearch_directory(directory,list_of_words):
	catelog_files(directory,list_of_words)
	save_dict_values_by_keys(file_type_catelog,file_type_list_dir)
	print("File type lists are saved")
	print("Filename Word Search in Progress..")
	wordsearch_dict_filename_lists()
	print("Filename Word Search Complete.")
	print("Saving List of Image Filenames with mached words..")
	save_dict_values_by_keys(word_matched_image_files,word_matched_image_list_dir)
	print("Image Filename Match lists saved")
	print("Saving List of Other Image Filenames..")
	save_dict_values_by_keys(other_image_files,other_image_list_dir)
	print("Other Image Filename lists saved")
	print("Saving List of other Matched Filenames..")
	save_dict_values_by_keys(word_matched_filenames,filename_word_match_list_dir)
	print("Other Matched Filename lists saved")
	print("----------------------------------")
	print("Now searching files for matches...")
	search_files_word_matches()
	print("Results:")
	for k in word_counts.keys():
		print('    %-7s %d' %(k,len(word_counts[k])))
	print("----------------------------------")
	print("Saving List of Files that had Matched Words..")
	save_dict_values_by_keys(word_matched_files,wordsearch_file_list_dir)
	print("Word Search File Lists saved")

def sub_matched_words_in_files():
	for k in word_matched_files.keys():
		sub_q = input("Replace " + k + "?").lower()
		if sub_q.startswith('y'):
			sub = input("Replace with:")
			print("Starting to replace " + k + " with " + sub)
			word_substitutions[k]=sub
			for f in word_matched_files[k]:
				print("->" + f)
				replace_words_in_file(f, k, sub, flags=0)
	print("Those are all the matches")
	return

def rename_matched_filenames():
	for k in word_matched_filenames.keys():
		if k in word_substitutions.keys():
			print("Previously replaced " + k + " with " + word_substitutions[k]")
			
			sub_q = input("Replace " + k + "?").lower()
			if sub_q.startswith('y'):
				use_previous_sub_q = input("Use " + word_substitutions[k] + " ?").lower()
				if use_previous_sub_q.startswith('y'):
					sub = word_substitutions[k]
				else:
					sub = input("Replace with:")
				print("Starting to replace " + k + " with " + sub)
				for filename in word_matched_filenames[k]:
					new_filename = replace_words_in_string(filename,k, sub, flags=0)
					os.rename(filename,new_filename)
	print("renaming files complete.")

def copycat_directory_files():
	wordsearch_directory(directory,list_of_words)
	sub_words_q = input('Want to substitute words found in files?').lower()
	if sub_words_q.startswith('y'):
		sub_matched_words_in_files()
	replace_word_matched_images_q = input("Want to replace word matched images?").lower()
	if replace_word_matched_images_q.startswith('y'):
		replace_images(word_matched_image_files)
	replace_other_images_q = input("Want to replace other images?").lower()
	if replace_other_images_q.startswith('y'):
		replace_images(other_image_files)
	rename_matched_filenames_q = input('Want to rename word matched filenames?').lower()
	if rename_matched_filenames_q.startswith('y'):
		rename_matched_filenames()
	
	


----------------------------------------------------------------------------
# mystring="walk walked walking talk talking talks talked fly flying"
# list_of_words=["walk","talk","fly"]

# word_counts = {}

# from nltk.stem.snowball import EnglishStemmer
# stemmer = EnglishStemmer()



# for target in list_of_words:
    # word_counts[target] = 0

    # for word in mystring.split(' '):

        # # Stem the word and compare it to the stem of the target
        # stem = stemmer.stem(word)        
        # if stem == stemmer.stem(target):
            # word_counts[target] += 1

# print word_counts
# Output:

# {'fly': 2, 'talk': 4, 'walk': 3}
# -----------------------------------------------------------------
# file_path="review.txt"
# text="boundation"
# subs="foundation"
# #calling the replace method
# replace(file_path, text, subs)
# -------------------------------------------------------------------------

# def checkKey(dict, key):
      
    # if key in dict.keys():
        # print("Present, ", end =" ")
        # print("value =", dict[key])
    # else:
        # print("Not present")
		
		
		

# from collections import defaultdict
  
# Details = defaultdict(list)
# Details["Country"].append("India")
