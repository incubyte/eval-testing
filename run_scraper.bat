@echo off
echo Installing required packages...
pip install -r scrape_requirements.txt

echo Running the DeepEval documentation scraper...
python scrape_deepeval_docs.py

echo Done! Documentation has been saved to the deepeval-docs folder.
pause
