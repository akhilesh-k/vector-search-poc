import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from zipfile import *
import json
from bs4 import BeautifulSoup

# PATH_PRODUCTS_DATASET = "data_encoder/data"
# # Name of the zip file (without .zip extension)
# NAME_DATASET = "data-3.json"

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def process_string(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    # Remove special characters and newlines
    text = re.sub(r'[\u2022\n<br>]', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize the text into words
    words = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    # Perform stemming
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in stemmed_words]
    # Join the processed words back into a single string
    processed_text = ' '.join(lemmatized_words)
    return processed_text

def process_colors(colorShade, colorList):
    # Convert colorShade to lowercase for case insensitivity
    colorList = []
    if colorShade is not None:
        colorShade = colorShade.lower()

    # Convert each color in colorList to lowercase for case insensitivity
    if colorList is not None:
        colorList = [color.lower() for color in colorList]

    # Add colorShade to colorList
    colorList.append(colorShade)

    # Get unique colors by converting the list to a set
    unique_colors = set(colorList)

    # Convert the set back to a string
    if (len(unique_colors) == 0):
        unique_colors_string = ', '.join(unique_colors)
        return unique_colors_string
    else:
        return ""

# def load_products_dataset():
#     with ZipFile(PATH_PRODUCTS_DATASET+"/"+NAME_DATASET+".zip") as dataZip:
#         with dataZip.open(NAME_DATASET, mode='r') as dataFile:
#             products_dataset = json.load(dataFile)
#     return products_dataset


# #### Load the original products dataset
# print(f'Loading the product dataset')
# products_dataset = load_products_dataset()

# for product in products_dataset:
#     print(f'{process_string(product.get("uniqueSellingPoint"))}')