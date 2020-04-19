Disclaimer: Due to a bug, the system cant be debugged if DEMorphy is included
Fortunate, it is only used in the preprocessing, so you can run the system once and do the
preprocessing (files are written to corpus/preprocessed) and debug the rest of the system
afterwards without preprocessing (it increases the performance, too).


How-To get the system running:

1. Get pip (sudo apt install python3-pip)
2. Get Spacy via pip (pip3 install -U spacy)
3. Load German Version (python3 -m spacy download de_core_news_sm)
4. Install de_morphy from github (https://github.com/DuyguA/DEMorphy/blob/master/README.md)
5. Decide if you want to do preprocessing and comment/uncomment the import in main
6. Run Main
7. The results of all texts combined are printed to the console
8. Results of the single texts can be found in corpus/resoluted

