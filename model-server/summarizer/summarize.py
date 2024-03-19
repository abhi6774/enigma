import os
from transformers import pipeline
from transformers.pipelines import TokenClassificationPipeline, AggregationStrategy
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer
)
import numpy as np
from logger import log
import requests
from summarizer.utils import split_text, extract_text_from_pdf
from exec_time import execution_time

summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")


def summarize_text(text: str):
    log("Summarizing text")
    summary = summarizer(text)
    log("Summary done")
    return summary


class KeyPhraseExtractionPipeline(TokenClassificationPipeline):

    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])

def extract_key_phrase(text: str):
    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = KeyPhraseExtractionPipeline(model=model_name)
    result = extractor(text.replace("\n", " "))
    key_entities = []
    for i in result:
        key_entities.append(i)
    return key_entities


def summarize(text: str, total_length: int):
    summary = ""

    if total_length > 800:
        splitted_text = split_text(text, total_length, 800)
        summary_pieces = []
        for st in splitted_text:
            summary_pieces.append(st)
        summary = summarize_with_mistral("".join(summary_pieces))
    else:
        summary = summarize_text(text)[0]["summary_text"]

    return summary


# summarize from pdf
def summarize_from_pdf(filename: str):
    final_text, totalLength = extract_text_from_pdf(filename)
    summary = summarize(final_text, totalLength)

    return {
        "summary": summary,
        "stl": len(summary),
        "original_text": final_text,
        "otl": totalLength
    }


@execution_time
def summarize_with_mistral(text: str) -> str:
    model_url = "https://api.mistral.ai/v1/chat/completions"
    key=os.environ.get("MISTRAL_KEY")
    response = requests.post(model_url, headers={
        "Authorization": f"Bearer {key}",
        "content-type": "application/json"
    }, json={
        "model":"open-mistral-7b",
        "messages": [{"role": "system", "content": "You are enigma an lawyer AI Assistant"},
        {"role": "user", "content": f"Summarize: {text}"} ]
    })
    result = response.json()
    return result["choices"][0]["message"]["content"]