# -*- coding: utf-8 -*-
#/usr/bin/python

import numpy as np
import math
from typing import *
import functools
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Méthode récursive -> meilleure complexité pour des grandes
#                      quantités avec peu de pièces possibles

# Bottom-up intéressante pour un grand nombre de pièces ou
# pour beaucoup de rendus successifs


#%%
def McNuggets(systeme):
    nbpieces = [0]
    liste = [[]]
    i=0
    sequence = 0
    while True:
        i+=1
        m = math.inf
        p = -1
        for piece in systeme:
            if i-piece<0: continue
            t=1+nbpieces[i-piece]
            if t<m:
                m=t
                p=piece
        if m==math.inf:
            nbpieces.append(math.inf)
            liste.append([])
            sequence = 0
            continue
        nbpieces.append(m)
        liste.append(liste[i-p]+[p])
        sequence+=1
        if(sequence==min(systeme)):
            break
                
    return i-min(systeme)


print(McNuggets([6, 9, 20]))

#%%

#@functools.lru_cache
def editingDistance(string1 : str, string2 : str):
    d = [[i if j==0 else j for j in range(len(string2)+1)] for i in range(len(string1)+1)]
    for i in range(1, len(d)):
        for j in range(1, len(d[i])):
            d[i][j] = d[i-1][j-1] if string1[i-1]==string2[j-1] else min(1+d[i-1][j], 1+d[i][j-1], 1+d[i-1][j-1])
    return d[len(string1)-1][len(string2)-1]

print(editingDistance("NAPOLEON BON APPART", "NAPOLEON BONAPARTE"))

#%%

dico_chemins = {}
def aux(grille, x, y):
    if (x, y) in dico_chemins: return dico_chemins[(x, y)]
    if y>=len(grille)-1: return grille[-1][x]
    m=0
    for i in range(0, 2):
        t = aux(grille, x+i, y+1)+grille[y][x]
        if t>m: m=t
    dico_chemins[(x, y)] = m
    return m

def copie(L):return [x[:] for x in L]


def somme_chemin(G):
    G2=copie(G)
    for i in range(1,len(G)):
        for j in range(len(G[i])):
            if j==0 : G2[i][j]+=G2[i-1][0]
            elif j==len(G[i])-1: G2[i][j]+=G2[i-1][j-1]
            else:
                G2[i][j]+=min(G2[i-1][j],G2[i-1][j-1],G[i-1][j+1])
    return G2


def seamCarving(path, x=50):
    img = mpimg.imread(path)[:,:,0]
    M = np.empty_like(img)
    N = np.empty_like(img)
    M[0,:]=img[0,:]
    M[:,0]=img[:,0]
    for i in range(1,len(M)-1):
        for j in range(1,len(M[i])-1):
            M[i,j] = np.sqrt((img[i,j-1]-img[i,j+1])**2+(img[i-1,j]-img[i+1,j])**2)+min(M[i-1,j-1], M[i-1,j], M[i-1,j+1])
    #chemin = aux(M, x, 10) #Trop lent
    chemin = somme_chemin(M)
    plt.imshow(chemin, cmap="gray")

os.chdir("U:/remy.fayet/Info/2022-2023/")
seamCarving("parc_small.jpg")
