# 🎬 Movie Recommendation System

A **content-based movie recommendation system** built using **Python, NLP, and Machine Learning**, deployed as an interactive web app using **Streamlit**.

---

## 🌐 Live Demo

👉 https://movie-recommendation-system-nmmznsackyuvidyu7dxzkp.streamlit.app/

---

## 📸 Demo

![App Screenshot](demo.png)

---

## 📌 Overview

This project recommends movies similar to a given movie based on features like:

* Genres
* Keywords
* Cast
* Director

It uses **Natural Language Processing (NLP)** and **cosine similarity** to find and suggest movies with similar content.

---

## 🚀 Features

* 🔍 Search for any movie
* 🎯 Get top similar movie recommendations
* 🧠 NLP-based feature extraction
* ⚡ Fast and efficient similarity computation
* ❌ Handles invalid movie inputs

---

## 🧠 How It Works

1. Load movie and credits datasets
2. Merge datasets based on movie title
3. Clean and preprocess data
4. Extract important features:

   * Genres
   * Keywords
   * Cast (top 3 actors)
   * Director
5. Combine features into a single **tags column**
6. Apply text preprocessing (lowercase, stemming)
7. Convert text into numerical vectors using **CountVectorizer**
8. Compute similarity using **cosine similarity**
9. Recommend top similar movies

---

## 🛠️ Technologies Used

* Python 🐍
* Pandas
* Scikit-learn
* NLTK
* Streamlit

---

## 📥 Dataset

This project uses the **TMDB 5000 Movie Dataset**.

🔗 https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

The dataset includes:

* Movie overview
* Genres
* Cast
* Crew
* Keywords

---

## ▶️ How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/charankotta32-star/movie-recommendation-system.git
```

2. Navigate to the project folder:

```bash
cd movie-recommendation-system
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

---

## 📌 Example

**Input:**

```
Avatar
```

**Output:**

```
Aliens  
Independence Day  
Titan A.E.  
Predators  
```

---

## 💡 Future Improvements

* 🎨 Improve UI/UX design
* 🎬 Add movie posters using API
* 🔍 Use TF-IDF for better accuracy
* 🌐 Deploy with database integration
* 🤖 Add hybrid recommendation system

---

## 👨‍💻 Author

**Charan Ram Sai**
B.Tech CSE (AI & ML), SRM University

---

## ⭐ Show Your Support

If you liked this project:

⭐ Star this repository
🍴 Fork it
📢 Share it

---

## 📬 Connect With Me

* GitHub: https://github.com/charankotta32-star


---
