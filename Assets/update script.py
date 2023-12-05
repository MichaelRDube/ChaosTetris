import urllib.request, sys, os

#if not os.path.isdir("Assets"):
#    os.mkdir("Assets")
    
#bring in assets
#print("Fetching assets...")
#print("\tFetching game_over.png...")
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/game_over.png', 'Assets/game_over.png')
#print("\tDone.")
#print("\tFetching score.png...")
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/score.png', 'Assets/score.png')
#print("\tDone.")
#print("\tFetching wow.png...")
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/wow.png', 'Assets/wow.png')
#print("\tDone.")

if not os.path.isfile('Assets/high_scores.txt'):
    #print("\tFetching high_scores.png...")
    urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/Assets/high_scores.txt', 'Assets/high_scores.txt')
    #print("\tDone.")
#else:
    #print("\thigh_scores.txt already exists in assets.")
    
#print("Fetching executables...")
#print("\tFetching Tetris.exe...")
#bring in the executable
urllib.request.urlretrieve('https://raw.github.com/MichaelRDube/ChaosTetris/main/dist/Tetris.exe', 'Tetris.exe')
#print("Done.")