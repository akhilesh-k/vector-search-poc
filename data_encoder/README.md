[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Data Encoder
==========================
### Data Encoding Process

This python utility with three main scripts can be used to generate and export the embeddings for the ecommerce products data (not added here for the obvious reasons.): `create_dataset.py` and `products.py` and `text_preprocessor.py`.

The `create_dataset.py` script is the main script that processes the dataset and adds the text vectors into the text vector field `product_vector` and image vectors into the image vector field `product_image_vector` into the dataset. The script delivers the vectorised product information as `products-vectors-<<dataset>>.json`.

The `products.py` script is a helper script with all the utility methods to extract desired fields of our interests from the dataset, render text and image encoding and allows users to configure the transformers to be used for encoding and can be customized to fit different needs.

The `text_preprocessor.py` provides functions for processing text data and colors in available for the products. It contains methods for cleaning and transforming text data, as well as handling colors in a case-insensitive manner

Currently, the encoding process uses the [CLIP](https://github.com/openai/CLIP) model from OpenAI to generate *image encoding* and renders a 768 dimensional encoding. For *text encoding* [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) has been used which renders a 384 dimensional encoding.