import pickle
import os
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from loguru import logger

from backend.models import DisasterTweet, Severity


class SeverityClassifier:
    def __init__(self, model_path: str = "models/severity_classifier.pkl"):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.load_model()

    def train(self, tweets: List[DisasterTweet]):
        """Train the classifier."""
        # Engineer labels
        texts = [t.text for t in tweets]
        labels = [self.derive_severity(t.text) for t in tweets]

        # Vectorize
        self.vectorizer = TfidfVectorizer(max_features=1000)
        X = self.vectorizer.fit_transform(texts)

        # Train
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2)
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        logger.info(f"Model trained. Accuracy: {acc:.2f}, F1: {f1:.2f}")

        # Save
        os.makedirs("models", exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump((self.model, self.vectorizer), f)

    def predict(self, tweet_text: str) -> Tuple[Severity, float]:
        """Predict severity."""
        if not self.model:
            return Severity.LOW, 0.0
        X = self.vectorizer.transform([tweet_text])
        pred = self.model.predict(X)[0]
        prob = max(self.model.predict_proba(X)[0])
        return Severity(pred), prob

    def derive_severity(self, text: str) -> str:
        """Derive severity from keywords."""
        text = text.lower()
        if any(word in text for word in ["trapped", "dying", "urgent"]):
            return "CRITICAL"
        elif any(word in text for word in ["help needed", "emergency"]):
            return "HIGH"
        elif any(word in text for word in ["damage", "assistance"]):
            return "MEDIUM"
        else:
            return "LOW"

    def load_model(self):
        """Load trained model."""
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model, self.vectorizer = pickle.load(f)
            logger.info("Model loaded.")
