# FOMC Transcript Analysis Pipeline

A Natural Language Processing (NLP) pipeline that analyzes Federal Open Market Committee (FOMC) press conference transcripts using Hugging Face transformers.

## Project Description

This project analyzes transcripts from the Federal Open Market Committee (FOMC) meetings to provide quick and easy-to-understand analysis. The FOMC "reviews economic and financial conditions, determines the appropriate stance of monetary policy, and assesses the risks to its long-run goals of price stability and sustainable economic growth."

### Features

1. **Web Scraping**: Downloads PDF transcripts from the official FOMC website
2. **PDF Processing**: Converts PDFs to text files for analysis
3. **Sentiment Analysis**: Analyzes the positivity-negativity sentiment of each FOMC meeting
4. **Text Summarization**: Generates concise summaries of each transcript using extractive summarization
5. **Question Answering**: Allows user to query specific information across all transcripts chronologically

## Installation

1. Clone the repository
2. Install required dependencies:

```bash
pip install requests tqdm beautifulsoup4 pdfplumber transformers datasets torch numpy plotly nltk ipywidgets
```

## Usage

### Analysis Pipeline

Open and run `proj7.ipynb` in Jupyter Notebook to:
- Download FOMC transcripts
- Convert PDFs to text files
- Generate summaries of transcripts 
- Analyze sentiment
- Ask questions about specific topics

## Models Used

The project utilizes three Hugging Face transformer models:

1. **Sentiment Analysis**: tabularisai/robust-sentiment-analysis
2. **Text Summarization**: Falconsai/text_summarization
3. **Question Answering**: consciousAI/question-answering-roberta-base-s-v2

## Example Usage

To query information about inflation rates across all transcripts:

```python
question = "What is the current rate of inflation? Only show me the exact number"
questAns = pipeline(model="consciousAI/question-answering-roberta-base-s-v2", device=device)

for file in textDict:
    answer = questAns(question=question, context=textDict[file])
    date = file[12:20]
    print(f"{date}: {answer['answer']}")
```

## Performance

- Average compression ratio for summaries: ~95%
- Question answering confidence: ~91% (for inflation rate queries)
- Processing time: ~30 minutes for complete pipeline execution

## Requirements

- Python 3.8+
- CUDA-capable GPU (optional, but recommended)
- Internet connection for downloading models and transcripts

## Notes

- The web scraper includes rate limiting to be respectful to the FOMC website
- PDF processing includes cleaning steps specific to FOMC transcript formatting
- Question answering performance varies based on query specificity and relevance

## License

This project is open source and available under the MIT License.
