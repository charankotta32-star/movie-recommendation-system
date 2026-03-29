# 🎬 Movie Recommendation System

A content-based movie recommendation system built using Python, Natural Language Processing (NLP), and machine learning techniques.

---

## 📌 Overview

This project recommends movies similar to a given movie based on content such as genres, keywords, cast, and director.

It uses text processing and similarity metrics to find movies with similar characteristics.

---

## 🚀 Features

* Recommend movies based on similarity
* Uses genres, keywords, cast, and director
* NLP-based preprocessing
* Clean and efficient implementation
* Handles invalid inputs

---

## 🧠 How It Works

1. Load and merge movie datasets
2. Clean and preprocess data
3. Extract important features (genres, keywords, cast, director)
4. Combine all features into a single “tags” column
5. Convert text into numerical vectors using CountVectorizer
6. Compute similarity using cosine similarity
7. Recommend top similar movies

---

## 🛠️ Technologies Used

* Python
* Pandas
* Scikit-learn
* NLTK

---

## ▶️ How to Run

1. Clone the repository:

```
git clone https://github.com/charankotta32-star/movie-recommendation-system.git
```

2. Install dependencies:

```
pip install pandas scikit-learn nltk
```

3. Run the script:

```
python main.py
```

---

## 📌 Example

Input:

```
recommend("Avatar")
```

Output:

```
Aliens
Predators
Titan A.E.
...
```

---

## 💡 Future Improvements

* Add web interface (Streamlit/Flask)
* Use TF-IDF for better recommendations
* Integrate movie API for real-time data
* Improve recommendation accuracy

---

## 👨‍💻 Author

**Charan Ram Sai**
B.Tech CSE (AI & ML), SRM University
