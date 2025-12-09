import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# 1. Load labeled sentiment datasets from text files
df_imdb = pd.read_csv('imdb_labelled.txt', sep='\t', header=None, names=['text', 'label'])
df_amzn = pd.read_csv('amazon_cells_labelled.txt', sep='\t', header=None, names=['text', 'label'])
df_yelp = pd.read_csv('yelp_labelled.txt', sep='\t', header=None, names=['text', 'label'])

# Combine all datasets into a single DataFrame
df = pd.concat([df_imdb, df_amzn, df_yelp], ignore_index=True)

# 2. Split the dataset into training and testing sets (80% train, 20% test)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

# Separate features (texts) and labels
train_texts = train_df['text'].values
train_labels = train_df['label'].values
test_texts = test_df['text'].values
test_labels = test_df['label'].values

# 3. Define a function to clean text (lowercase, remove non-alphanumeric characters)
def clean_text(s):
    s = s.lower()
    s = re.sub(r'[^0-9a-z\s]', '', s)
    return s

# Apply text cleaning
train_texts_clean = [clean_text(s) for s in train_texts]
test_texts_clean = [clean_text(s) for s in test_texts]

# 4. Convert text to TF-IDF feature vectors
vectorizer = TfidfVectorizer(stop_words=None)  # keep stopwords for polarity (e.g., "not")
X_train = vectorizer.fit_transform(train_texts_clean)
X_test = vectorizer.transform(test_texts_clean)

print("Number of training samples:", X_train.shape[0])
print("Number of features (vocabulary size):", X_train.shape[1])

# 5. Train a Logistic Regression model
log_clf = LogisticRegression(max_iter=1000, random_state=0)
log_clf.fit(X_train, train_labels)

# 6. Train a Feedforward Neural Network (MLP) model
nn_clf = MLPClassifier(
    hidden_layer_sizes=(16,),
    activation='relu',
    solver='adam',
    max_iter=300,
    random_state=0
)
nn_clf.fit(X_train, train_labels)

# 7. Predict sentiment on test set using both models
log_preds = log_clf.predict(X_test)
nn_preds = nn_clf.predict(X_test)

# 8. Display predictions and accuracy
print("\nLogistic Regression Prediction Sample:")
print(log_preds[:10])
print("Accuracy:", accuracy_score(test_labels, log_preds))

print("\nNeural Network Prediction Sample:")
print(nn_preds[:10])
print("Accuracy:", accuracy_score(test_labels, nn_preds))
