from transformers import pipeline
from transformers.pipelines import TokenClassificationPipeline, AggregationStrategy
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer
)
import numpy as np

summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

def _summarize_text(text: str):
    print("Summarizing text")
    summary = summarizer(text)
    print("Summary done")
    return summary

class KeyphraseExtractionPipeline(TokenClassificationPipeline):

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
    

