import streamlit as st
import requests

WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"


@st.cache_data
def load_words():
    response = requests.get(WORD_LIST_URL)
    words = response.text.splitlines()

    filtered = [
        w.strip().lower()
        for w in words
        if len(w.strip()) == 5 and w.isalpha()
    ]

    return filtered


def wordle_solver(excluded_letters, confirmed_letters, position_pattern, word_list):
    excluded = set(excluded_letters.lower())
    confirmed = set(confirmed_letters.lower())

    results = []

    for word in word_list:
        letters = set(word)

        # rule 1: excluded letters
        if letters & excluded:
            continue

        # rule 2: must include confirmed letters
        if not confirmed.issubset(letters):
            continue

        # rule 3: green position check
        if position_pattern != "x":
            match = True

            for i in range(5):
                if position_pattern[i] != "-":
                    if word[i] != position_pattern[i].lower():
                        match = False
                        break

            if not match:
                continue

        results.append(word)

    return results


# ---------------- UI ----------------

st.title("Wordle Solver")
st.write("Find possible 5 letter words based on obtained clues")

words = load_words()

st.subheader("Step 1 - Excluded letters (gray letters)")
excluded = st.text_input("Letters that are NOT in the word (For example: abcxyz)")

st.subheader("Step 2 - Confirmed letters (yellow letters)")
confirmed = st.text_input("Letters that MUST be in the word (For example: fopq)")

st.subheader("Step 3 - Green letters (position pattern)")
st.write("Use `-` for unknown positions, or type `x` to skip")
position = st.text_input("Pattern (For example: a_i_e or 'x')").replace(" ", "")

if st.button("Solve"):
    results = wordle_solver(excluded, confirmed, position, words)

    st.subheader("Possible Words")

    if results:
        st.write(f"Total: {len(results)} words")
        
        for i, word in enumerate(results, start=1):
            st.markdown(f"**{i}. {word}**")
            
    else:
        st.warning("No words found 😢")

