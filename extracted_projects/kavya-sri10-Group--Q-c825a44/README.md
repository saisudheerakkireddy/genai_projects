# AI-Health-Chatbot


💡 Ever wondered if Artificial Intelligence can act like a doctor? In this video, I’ll show you how I built an AI-powered Healthcare Chatbot that can predict diseases from symptoms using Machine Learning in Python. 🚑
We’ll go step by step:
✅ Symptom extraction with NLP
✅ Training a Machine Learning model (Random Forest Classifier)
✅ Building an interactive chatbot to ask follow-up questions
✅ Disease prediction with confidence score
✅ Giving precautions, health tips, and an end motivational quote 💬


Build a chatbot interface (with follow-up questions & advice)

Integrate AI into a user-friendly healthcare solution

📌 Technologies used: Python, Scikit-learn, Pandas, NLP, Machine Learning

Start 💬
│
├── 🔹 User Input

│     └── "I have a sore throat and mild fever"

│

├── 🧩 NLP Processing (Text → Symptoms)

│     ├── Tokenization

│     ├── Lemmatization

│     └── Symptom Extraction → [fever, sore_throat]
│

├── 📊 Data Preprocessing

│     ├── Encode symptoms (multi-hot vector)

│     ├── Encode diseases (label encoding)

│     └── Train-test split

│
├── 🤖 Machine Learning Model

│     ├── Random Forest Classifier

│     ├── Train on symptom-disease dataset

│     └── Evaluate accuracy, precision, recall

│
├── 🧮 Prediction

│     ├── Input: extracted symptoms → model

│     ├── Output: Predicted disease

│     └── Confidence score (e.g., 92%)

│
├── 🔁 Chatbot Logic

│     ├── If confidence < threshold → ask follow-up

│     │     └── "Do you also have fatigue or body pain?"

│     └── Update symptoms → re-run prediction

│
├── 💡 Health Advice Module

│     ├── Disease info

│     ├── Precautions

│     ├── Diet & treatment tips

│     └── Motivational quote

│
├── 💻 User Interface

│     ├── Web app (Streamlit / Flask / Gradio)

│     └── Interactive chatbot (text or voice)

│
├── 🚀 Deployment

│     ├── Streamlit Cloud / Render / Hugging Face

│     └── Shareable healthcare assistant

│
└── ✅ End Result
      ├── AI predicts disease from symptoms
      
      ├── Provides health advice
      
      └── Acts as a virtual medical assistant 🩺


