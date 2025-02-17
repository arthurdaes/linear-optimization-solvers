import numpy as np

import tkinter as tk
from tkinter import messagebox

from simplex import simplex_method, SIMPLEX_MIN, SIMPLEX_MAX
from gui import GUIBuilder

def main():
    c = [40, 30]
    
    A = [
        [1, 1],
        [2, 1],
    ]
    b = [12, 16]

    x, z = simplex_method(c, A, b)

    print("x =", x)
    print("z =", z)

if __name__ == "__main__":
    main()
