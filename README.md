## Overview

This project implements a Vector Space Model (VSM) for information retrieval. The VSM represents documents and queries as vectors in a multi-dimensional space, where each dimension corresponds to a term. It computes the similarity between documents and queries to rank the documents based on relevance to the query.

## Features

- **Text Preprocessing:** Utilizes text preprocessing techniques from the previous project, including SGML tag removal, tokenization, stopword removal, and stemming.
- **Inverted Index Construction:** Constructs an inverted index to efficiently store and retrieve document-term frequencies.
- **TF-IDF Weighting:** Computes TF-IDF (Term Frequency-Inverse Document Frequency) weights to assign importance to terms in documents and queries.
- **Document Retrieval:** Retrieves relevant documents for given queries using the Vector Space Model.
- **Output Generation:** Generates output files containing ranked lists of documents for each query based on their relevance scores.

## How to Use

1. **Clone the Repository:** Clone this repository to your local machine.
   ```bash
   git clone https://github.com/andrerod22/486-vector-space.git

2. **Install Dependencies:** Ensure you have Python installed, aalong with any dependencies required by the project.
3. **Run the Script:** Execute vectorspace.py script and provide the necessary command-line arguments.
                       python vectorspace.py [weight_docs] [weight_queries] [input_directory] [queries_file]
                       •	[weight_docs]: Weighting scheme for documents (tf, tfc).
	                   •	[weight_queries]: Weighting scheme for queries (idf, tfx).
	                   •	[input_directory]: Path to the directory containing document files.
	                   •	[queries_file]: Path to the file containing queries.
4. **View Output:** The script will generate output files with ranked lists of documents for each query based on their relevance scores.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
The text preprocessing techniques used in this project are adapted from the previous project see implementation at https://github.com/andrerod22/486-text-preprocessing 

## Contact
For any inquiries or questions, please contact andre.rodriguez9722@outlook.com