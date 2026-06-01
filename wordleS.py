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


def wordle_solver(
    excluded_letters,
    confirmed_letters,
    position_pattern,
    yellow_pattern,
    word_list
):
    excluded = set(excluded_letters.lower())
    confirmed = set(confirmed_letters.lower())

    results = []

    for word in word_list:
        letters = set(word)

        # Rule 1: Excluded letters
        if letters & excluded:
            continue

        # Rule 2: Must include confirmed letters
        if not confirmed.issubset(letters):
            continue

        # Rule 3: Green position check
        if position_pattern != "x":
            match = True

            for i in range(5):
                if position_pattern[i] != "-":
                    if word[i] != position_pattern[i].lower():
                        match = False
                        break

            if not match:
                continue

        # Rule 4: Yellow position check
        # Letter exists but CANNOT be in this position
        if yellow_pattern != "x":
            match = True

            for i in range(5):
                if yellow_pattern[i] != "-":
                    if word[i] == yellow_pattern[i].lower():
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
excluded = st.text_input(
    "Letters that are NOT in the word (For example: abcxyz)"
)

st.subheader("Step 2 - Confirmed letters (yellow / green letters)")
confirmed = st.text_input(
    "Letters that MUST be in the word (For example: fopq)"
)

st.subheader("Step 3 - Green letters (correct positions)")
st.write("Use '-' for unknown positions, or type 'x' to skip")

position = st.text_input(
    "Pattern (For example: a--i- or 'x')"
).replace(" ", "")

st.subheader("Step 4 - Yellow letters (wrong positions)")
st.write(
    "Place letters where they CANNOT be.\n\n"
    "Example: h--l- means H cannot be position 1 and L cannot be position 4.\n\n"
    "Use '-' for unknown positions, or type 'x' to skip."
)

yellow_pattern = st.text_input(
    "Pattern (For example: h--l- or 'x')"
).replace(" ", "")

if st.button("Solve"):

    if position != "x" and len(position) != 5:
        st.error("Green pattern must be exactly 5 characters.")
        st.stop()

    if yellow_pattern != "x" and len(yellow_pattern) != 5:
        st.error("Yellow pattern must be exactly 5 characters.")
        st.stop()

    results = wordle_solver(
        excluded,
        confirmed,
        position,
        yellow_pattern,
        words
    )

    st.subheader("Possible Words")

    if results:
        st.write(f"Total: {len(results)} words")

        for i, word in enumerate(results, start=1):
            st.markdown(f"**{i}. {word}**")

    else:
        st.warning("No words found 😢")