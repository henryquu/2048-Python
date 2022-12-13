from gui import Board

if __name__ == '__main__':

    print("Movement:",
    "W or w to move up",
    "S or s to move down",
    "D or d to move right",
    "A or a to move left", 
    "\n", sep = "\n"
    )

    board1 = Board(4)
    

    while True:
        if board1.randomly_add_2or4():
            board1.show()
            board1.move()
        else: 
            break
