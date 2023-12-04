import urllib.request, sys, os

#if not os.path.isdir("Assets"):
#    os.mkdir("Assets")
    
#bring in assets
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/game_over.png', 'game_over.png')
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/score.png', 'Assets/score.png')
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/wow.png', 'Assets/wow.png')

#bring in the executable
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Minimal%20Package/Tetris.exe', 'Tetris.exe')
