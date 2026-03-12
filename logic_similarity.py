import tokenize
import io
from difflib import SequenceMatcher
import keyword

# Only Python normalization implemented for now
def normalize_python_code(code):
    var_mapping = {}
    var_count = 0
    tokens = []

    try:
        g = tokenize.generate_tokens(io.StringIO(code).readline)
        for toknum, tokval, _, _, _ in g:
            if toknum == tokenize.NAME:
                if keyword.iskeyword(tokval):
                    tokens.append(tokval)
                else:
                    if tokval not in var_mapping:
                        var_mapping[tokval] = f"VAR{var_count}"
                        var_count += 1
                    tokens.append(var_mapping[tokval])
            elif toknum == tokenize.NUMBER:
                tokens.append(tokval)
            elif toknum == tokenize.OP:
                tokens.append(tokval)
    except:
        tokens = code.lower().split()

    return tokens

def compute_similarity(code1, code2, language="python"):
    tokens1 = normalize_python_code(code1)
    tokens2 = normalize_python_code(code2)

    if len(tokens1) == 1 and len(tokens2) == 1:
        return 100 if tokens1[0] == tokens2[0] else 0

    sm = SequenceMatcher(None, tokens1, tokens2)
    similarity = sm.ratio()
    return round(similarity * 100, 2)
