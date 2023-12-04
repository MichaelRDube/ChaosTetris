import urllib.request, sys, os

#if not os.path.isdir("Assets"):
#    os.mkdir("Assets")
    
#bring in assets
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/game_over.png', 'Assets/game_over.png')
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/score.png', 'Assets/score.png')
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/wow.png', 'Assets/wow.png')
if not os.path.isfile('Assets/high_scores.txt'):
    urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/high_scores.txt', 'Assets/high_scores.txt')

#bring in the executable
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/dist/Tetris.exe', 'Tetris.exe')
