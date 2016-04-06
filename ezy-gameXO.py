import random


board = [0,1,2,
         3,4,5,
         6,7,8]

def show():
    print (board[0],'|',board[1],'|',board[2])
    print ('---------')
    print (board[3],'|',board[4],'|',board[5])
    print ('---------')
    print (board[6],'|',board[7],'|',board[8])

def checkLine(char, spot1, spot2, spot3):
    if board[spot1] == char and board[spot2] == char and board[spot3] == char:
        # print board[spot1],':',board[spot2],':',board[spot3]
        return True

def checkWin(char):
    if checkLine(char,0,1,2):
        return True
    if checkLine(char,3,4,5):
        return True
    if checkLine(char,6,7,8):
        return True

    if checkLine(char,0,3,6):
        return True
    if checkLine(char,1,4,7):
        return True
    if checkLine(char,2,5,8):
        return True

    if checkLine(char,0,4,8):
        return True
    if checkLine(char,2,4,6):
        return True

def spot(char, key):
    if board[key] != 'X' and board[key] != 'O':
        board[key] = char
        return True
    else:
        return False

def GameStart():
    Exit = False
    show()
    while not Exit:

        #ตาเดินของ X
        while True:
            key = input("Select a spot (X): ")
            key = int(key)

            if spot('X', key) == True:
                show()
                if checkWin('X') == True:
                    print("~~~~ X WIN ~~~~")
                    Exit = True
                break
            else:
                print ('This spot is taken!')

        # ตรวจสอบจบเกมส์
        if Exit == True:
            break

        #ตาเดินของ O
        while True:
            key = input("Select a spot (O): ")
            key = int(key)

            if spot('O', key) == True:
                show()
                if checkWin('O') == True:
                    print("~~~~ O WIN ~~~~")
                    Exit = True
                break
            else:
                print ('This spot is taken!')
