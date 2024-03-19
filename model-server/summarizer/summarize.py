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


def summarize(text: str, total_length: int):
    summary = ""

    if total_length > 800:
        splitted_text = split_text(text, total_length, 800)
        summary_pieces = []
        for t in splitted_text:
            log("T\n\n", t)
            summary_pieces.append(summarize_with_llama(t))
        summary = summarize_with_llama("".join(summary_pieces))
    else:
        summary = summarize_text(text)

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


def summarize_with_llama(text: str) -> str:
    model_url = "https://api.cloudflare.com/client/v4/accounts/1c7120b407404a4d257e57af5a88f88f/ai/run/@cf/meta/llama-2-7b-chat-fp16"
    response = requests.post(model_url,
        headers={"Authorization": f"Bearer 3ti0Lh8dnLmIpbGi-0n7Z9o58JAoBgkBQh3k9tPh"},
        json={
            "messages": [
                {"role": "system", "content": "You are enigma an lawyer AI Assistant"},
                {"role": "user", "content": f"Summarize: {text}"}
            ]
        }
    )

    result = response.json()
    if result["success"]:
        log(result["result"]["response"])
        return result["result"]["response"]
    return result
