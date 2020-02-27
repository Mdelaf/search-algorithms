from grid import GraphicGrid

HEIGHT = 25
WIDTH = 40
ALLOW_DIAGONALS = False
INTERVAL = 0.02


app = GraphicGrid(height=HEIGHT, width=WIDTH, allow_diagonals=ALLOW_DIAGONALS,
                  interval=INTERVAL)
app.mainloop()
