import requests
import os

# download a list of identifier
base_url = "https://archive.org/advancedsearch.php?q="
components = {
    "q": "contributor:The+Library+of+Congress",
    "rows": 5,
    "page": 1,
    "output": "csv",
    "fl": "identifier"
}

r = requests.get(base_url, params=components)
identifiers = [ident.strip('"') for ident in r.text.split()[1:]]

# make a directory to store the file
try:
    os.mkdir("ArchiveDownloads")
except OSError:
    pass

# switch to that director
os.chdir("ArchiveDownloads")

# write identifiers to file
with open('itemlist.txt', 'w') as outfile:
    outfile.write('\n'.join(identifiers))

# download to the directory
os.system("wget -r -H -nc -np -nd -nH --cut-dirs=1 -A .pdf -e robots=off "
          "-l1 -i ./itemlist.txt -B 'http://archive.org/download/'")

# clean up the downloads by removing pdfs which also
# have a black and white copy and the itemlist
files = os.listdir('.')

to_remove = ["itemlist.txt"]
for fname in files:
    if fname.endswith("_bw.pdf"):
        to_remove.append(fname[:-len("_bw.pdf")] + ".pdf")

os.system("rm %s" % (" ".join(to_remove)))
