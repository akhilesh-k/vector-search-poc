#!/usr/bin/env python3

import json
import io
import requests
from zipfile import *
from sentence_transformers import SentenceTransformer
from PIL import Image
from transformers import CLIPTokenizer
import torch
import clip
from tqdm import tqdm
import text_preprocessor

PATH_PRODUCTS_DATASET = "data_encoder/data"
# Name of the zip file (without .zip extension)
NAME_DATASET = "data-1.json"
PATH_PRODUCTS_MODEL = "all-MiniLM-L6-v2"

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-L/14', device)


def load_products_dataset():
    with ZipFile(PATH_PRODUCTS_DATASET+"/"+NAME_DATASET+".zip") as dataZip:
        with dataZip.open(NAME_DATASET, mode='r') as dataFile:
            products_dataset = json.load(dataFile)
    return products_dataset


def get_product_sentence(model, product):
    color = text_preprocessor.process_colors(
        product.get('colorShade'), product.get('colorList'))
    fields = [product.get('nameSearch'), product.get('merchantName'),
              product.get('brand'), product.get('city'), text_preprocessor.process_string(product.get('uniqueSellingPoint')), color]
    if fields[0] is None:
        fields[0] = product.get('name')
    non_empty_fields = [field for field in fields if field is not None]

    if non_empty_fields:
        return ' '.join(non_empty_fields)
    else:
        return ""


def get_products_sentences(model, products_dataset):
    return [get_product_sentence(model, product) for product in tqdm(products_dataset, desc="Calculating product vectors")]

def get_product_image(product):
    product_img = f"{(product['mediumImage'])}"
    return "http://www.static-src.com/wcsstore/Indraprastha/images/catalog/full" + product_img


def load_products_embedding_model():
    return SentenceTransformer(PATH_PRODUCTS_MODEL)


def calculate_product_vector(model, product):
    product_sentence = get_product_sentence(product)
    return model.encode(product_sentence)


def calculate_products_vectors(model, products_dataset):
    products_sentences = get_products_sentences(model, products_dataset)
    return model.encode(products_sentences)


def calculate_product_image_vectors(product):
    try:
        image = get_product_image(product)
        r = requests.get(image, stream=True)
        # Load and preprocess the image
        validated_image = Image.open(r.raw)
        preprocess_image = preprocess(validated_image).unsqueeze(0).to(device)
        # Encode the image
        with torch.no_grad():
            image_encoding = model.encode_image(preprocess_image)[0]
            # print(image_encoding)
            return image_encoding
    except Exception:
        return []


def calculate_products_image_vectors_clip(products_dataset):
    products_images = []
    for product in tqdm(products_dataset, desc="Calculating product image vectors"):
        product_image_vector = calculate_product_image_vectors(product)
        products_images.append(product_image_vector)
    return products_images


def export_products_json(products_dataset):
    # Serializing json
    json_object = json.dumps(products_dataset, indent=2)
    # Writing to dataset.json
    with open(PATH_PRODUCTS_DATASET+"/"+"products-vectors-"+NAME_DATASET, "w") as outfile:
        outfile.write(json_object)


def truncate_sentence(sentence, tokenizer):
    """
    Truncate a sentence to fit the CLIP max token limit (77 tokens including the
    starting and ending tokens).

    Args:
        sentence(string): The sentence to truncate.
        tokenizer(CLIPTokenizer): Retrained CLIP tokenizer.
    """

    cur_sentence = sentence
    # print("new doc",cur_sentence)
    tokens = tokenizer.encode(cur_sentence)

    if len(tokens) > 77:
        # Skip the starting token, only include 75 tokens
        truncated_tokens = tokens[1:76]
        cur_sentence = tokenizer.decode(truncated_tokens)
        # Recursive call here, because the encode(decode()) can have different result
        return truncate_sentence(cur_sentence, tokenizer)

    else:
        return cur_sentence
