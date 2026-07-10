"""
NLP Sentiment Analysis Engine.
Uses HuggingFace transformers to analyze tweet text.
"""

from transformers import pipeline


class SentimentAnalyzer:
    def __init__(self):
        print("Loading NLP model (first run downloads ~500MB)...")
        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
            device=-1
        )
        print("Model loaded")
    
    def analyze_text(self, text):
        result = self.classifier(text[:512])[0]
        label = result['label'].lower()
        score = result['score']
        
        scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
        
        if label == 'positive':
            scores['positive'] = score
            scores['negative'] = (1 - score) * 0.3
            scores['neutral'] = (1 - score) * 0.7
        elif label == 'negative':
            scores['negative'] = score
            scores['positive'] = (1 - score) * 0.3
            scores['neutral'] = (1 - score) * 0.7
        else:
            scores['neutral'] = score
            scores['positive'] = (1 - score) * 0.5
            scores['negative'] = (1 - score) * 0.5
        
        return scores
    
    def analyze_tweets(self, tweets):
        if not tweets:
            return {'positive': 0, 'negative': 0, 'neutral': 0, 'compound': 0}
        
        total = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for tweet_text in tweets:
            scores = self.analyze_text(tweet_text)
            for key in total:
                total[key] += scores[key]
        
        n = len(tweets)
        avg = {k: round(v / n, 4) for k, v in total.items()}
        avg['compound'] = round(avg['positive'] - avg['negative'], 4)
        
        return avg


_analyzer = None

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer