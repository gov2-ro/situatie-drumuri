Situația drumurilor naționale și a autostrăzilor din România. https://andnet.ro/dispecerat/

w nicer GUI / UX

__downloadTables.py__
baseurl='https://dispecerat.andnet.ro/'
download_folder = '/Users/pax/devbox/gov2/data/situatie-drumuri/raw'

__scrapeData.py__
cachedFile = "data/raw/_last.html"
outfolder = "data/json/"

__buildNice.py__ (package error 230810)
sourceJson = "data/json/latest.json"
outputJson = "data/rez.json"
mbaseurl = "https://andnet.ro/dispecerat/dispecerat.php" (not available)
mbaseurl = "https://dispecerat.andnet.ro/" (??)