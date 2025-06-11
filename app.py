import streamlit as st
import pandas as pd
import gzip

@st.cache_data
def load_movies():
    with gzip.open("datasets/title.basics.tsv.gz", "rt", encoding="utf-8") as f:
        df = pd.read_csv(f, sep="\t", na_values="\\N")
        df = df[df["titleType"].isin(["movie", "tvMovie"])]
        return df

@st.cache_data
def load_ratings():
    with gzip.open("datasets/title.ratings.tsv.gz", "rt", encoding="utf-8") as f:
        df = pd.read_csv(f, sep="\t")
        return df

st.title("🎬 IMDB Movie Explorer")

movies_df = load_movies()
ratings_df = load_ratings()

merged_df = pd.merge(movies_df, ratings_df, on="tconst", how="inner")
merged_df = merged_df.dropna(subset=["primaryTitle", "startYear", "averageRating"])

title_input = st.text_input("Search for a movie:")

if title_input:
    results = merged_df[merged_df["primaryTitle"].str.contains(title_input, case=False, na=False)]
    for idx, row in results.iterrows():
        st.subheader(f"{row['primaryTitle']} ({int(row['startYear'])})")
        st.text(f"Genres: {row['genres']}")
        st.text(f"Runtime: {row['runtimeMinutes']} mins")
        st.text(f"Rating: ⭐ {row['averageRating']}/10 ({row['numVotes']} votes)")
        st.markdown("---")
