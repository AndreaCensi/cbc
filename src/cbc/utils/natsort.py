# ---------------------------------------------------------
# natsort.py: Natural string sorting.
# ---------------------------------------------------------

# By Seo Sanghyeon.  Some changes by Connelly Barnes.
# Some more changes (key) by Andrea Censi.


def try_int(s):
    "Convert to integer if possible."
    try:
        return int(s)
    except:
        return s


def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    return map(try_int, re.findall(r'(\d+|\D+)', s))


def natcmp(a, b):
    "Natural string comparison, case sensitive."
    return cmp(natsort_key(a), natsort_key(b))


def natcasecmp(a, b):
    "Natural string comparison, ignores case."
    return natcmp(a.lower(), b.lower())


def natsort(seq, kcmp=natcmp, key=None):
    "In-place natural string sort."
    seq.sort(kcmp, key)


def natsorted(seq, kcmp=natcmp, key=None):
    "Returns a copy of seq, sorted by natural string sort."
    # convert set -> list
    temp = list(seq)
    natsort(temp, kcmp, key)
    return temp

