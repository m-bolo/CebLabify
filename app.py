from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def syllabify():
    word = request.form.get('input')  # Retrieve the word from the form
    syllables, sequences = get_syllables(word)  # Calculate syllables and sequences
    return render_template('index.html', words=word, syllables=syllables, sequences=sequences)


def get_CV_sequence(word):
    word = word.lower()
    vowels = ["a", "e", "i", "o", "u"]
    consonants = ["p", "t", "k", "b", "d", "g", "m", "n", "ng", "s", "h", "l", "r", "w", "y", "c"]
    consonant_clusters = ["pw", "py", "pr", "pl", "tw", "ty", "tr", "ts", "kw", "ky", "kr", "kl", "bw", "by", "br", "bl", "dw", "dy", "dr", "gw", "gr", "mw", "my", "nw", "ny", "sw", "sy", "hw"]

    prev_cons = None
    cv_seq = ""


    words = word.split("-")
    for w in words:
        for i, char in enumerate(w):
            if char not in vowels and char not in consonants:
                continue
            elif prev_cons == "n" and char == "g":
                prev_cons = "ng"
                continue
            elif prev_cons == "ng" and char in consonants:
                prev_cons = char
                cv_seq += "C"
            elif prev_cons == "sy" and char in vowels:
                prev_cons = None
                cv_seq += "V"
            elif prev_cons == "sy" and char in consonants:
                prev_cons = None
                cv_seq += "C"
            elif prev_cons and char in vowels:
                prev_cons = None
                cv_seq += "V"
            elif prev_cons and prev_cons + char in consonant_clusters:
                prev_cons = None
                cv_seq += "C"
            elif char in consonants:
                prev_cons = char
                cv_seq += "C"
            elif char in vowels:
                prev_cons = None
                cv_seq += "V"


    return cv_seq

def get_syllables(word):
    word = word.upper()
    words = word.split("-")
    sequences = []
    syllables = []

    for w in words:
        syl_seq = get_CV_sequence(w)
        while "CVCCV" in syl_seq:
            syl_seq = syl_seq.replace("CVCCV","CVC-CV")
        while "VCV" in syl_seq:
            syl_seq = syl_seq.replace("VCV","V-CV")
        while "VV" in syl_seq:
            syl_seq = syl_seq.replace("VV","V-V")
        while "CCVCCV" in syl_seq:
            syl_seq = syl_seq.replace("CCVCCV","CCVC-CV")
        while "CCVCV" in syl_seq:
            syl_seq = syl_seq.replace("CCVCV","CCV-CV")
        while "VCC" in syl_seq:
            syl_seq = syl_seq.replace("VCC","VC-C")
        while "CVCV" in syl_seq:
            syl_seq = syl_seq.replace("CVCV","CV-CV")
        while "VVC" in syl_seq:
            syl_seq = syl_seq.replace("VVC","V-VC")

        
        # # # Replace 'syo' with 'syon'
        # syl_seq = syl_seq.replace('CVC-CV', 'CVC-CVC')
        # # #syl_seq = syl_seq.replace('CVC-CVC', 'CVC-CV')
        # syl_seq = syl_seq.replace('CVC-CVC', 'CV-CCV')
        for cv in syl_seq.split("-"):
            sequences.append(cv)


        syl_seq_arr = syl_seq.split("-")
        i = 0
        for syl in syl_seq_arr:
            chars = len(syl)
            if "ng" in w[i:i+chars+1]:
                syllables.append(w[i:i+chars+1])
                i += chars+1
            else:
                syllables.append(w[i:i+chars])
                i += chars


    return [syllables, sequences]


# if __name__ == "__main__":
#     file = open('/content/drive/MyDrive/Python_Projects/test2/data.txt', 'r')
#     lines = file.readlines()
#     for line in lines:
#         word = line.strip()
#         syllables, sequences = get_syllables(word)
#         # print("Word: {} --> {}, {}".format(word, syllables, sequences))

if __name__ == '__main__':
    app.run(debug=True)