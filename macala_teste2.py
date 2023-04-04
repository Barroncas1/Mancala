import random
import time
#import numpy as np
from copy import deepcopy
from sys import exit
from pygame.locals import *
import sys
import pygame


PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')

NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
            'G': '2', '2': 'A'}  # para onde as peças vão em ordem anti horaria

OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                'K': 'E', 'L': 'F'}  # casa paralela do oponente, usada para regra de pegar as pedras do oponente

PIT_LABELS = 'ABCDEF1LKJIHG2'

STARTING_NUMBER_OF_STONES = 4  # trocar o numero de pedras: diferentes modos

pygame.init()

largura = 1400
altura = 788

tela = pygame.display.set_mode((largura, altura))
tela.fill((255, 255, 255))

cor_texto = (0, 0, 0)
tamanho_da_fonte = 75
fonte = pygame.font.Font(None, tamanho_da_fonte)

class State:


    def __init__(self):
        
        self.board = self.getNewBoard()
        self.display = self.displayBoard(self.board)
        self.player_turn = '1'

    def getNewBoard(self):
         s = STARTING_NUMBER_OF_STONES
         return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
                'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}  # tabuleiro inicial
    
    def displayBoard(self, board):
        stoneAmounts = []

        for pit in 'GHIJKL21ABCDEF':
            numStonesInThisPit = str(board[pit])
            stoneAmounts.append(numStonesInThisPit)

        posicao_mancala = 436
        posicao_1y = 557
        posicao_2y = 315

        tabuleiro_img = pygame.image.load("tabuleiro_3.png")
        tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
        tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
        tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
        pygame.display.flip()

        texta = fonte.render(str(stoneAmounts[8]), True, cor_texto)
        tela.blit(texta, (368, posicao_1y))

        textb = fonte.render(str(stoneAmounts[9]), True, cor_texto)
        tela.blit(textb, (493, posicao_1y))

        textc = fonte.render(str(stoneAmounts[10]), True, cor_texto)
        tela.blit(textc, (618, posicao_1y))

        textd = fonte.render(str(stoneAmounts[11]), True, cor_texto)
        tela.blit(textd, (743, posicao_1y))

        texte = fonte.render(str(stoneAmounts[12]), True, cor_texto)
        tela.blit(texte, (868, posicao_1y))

        textf = fonte.render(str(stoneAmounts[13]), True, cor_texto)
        tela.blit(textf, (993, posicao_1y))

        textg = fonte.render(str(stoneAmounts[5]), True, cor_texto)
        tela.blit(textg, (993, posicao_2y))

        texth = fonte.render(str(stoneAmounts[4]), True, cor_texto)
        tela.blit(texth, (868, posicao_2y))

        texti = fonte.render(str(stoneAmounts[3]), True, cor_texto)
        tela.blit(texti, (743, posicao_2y))

        textj = fonte.render(str(stoneAmounts[2]), True, cor_texto)
        tela.blit(textj, (618, posicao_2y))

        textk = fonte.render(str(stoneAmounts[1]), True, cor_texto)
        tela.blit(textk, (493, posicao_2y))

        textl = fonte.render(str(stoneAmounts[0]), True, cor_texto)
        tela.blit(textl, (368, posicao_2y))

        text1 = fonte.render(str(stoneAmounts[7]), True, cor_texto)
        tela.blit(text1, (1118, posicao_mancala))

        text2 = fonte.render(str(stoneAmounts[6]), True, cor_texto)
        tela.blit(text2, (243, posicao_mancala))

        pygame.display.update()

    def askForPlayerMove(self, board):
        
        while True:
            # pedir uma jogada
            if self.player_turn == '1':
                textMove1a = fonte.render(
                    '1                                   A - F', True, cor_texto)
                tela.blit(textMove1a, (493, 50))
                pygame.display.update()

            elif self.player_turn == '2':
                textMove2 = fonte.render(
                    '2                                   G - L', True, cor_texto)
                tela.blit(textMove2, (493, 50))
                pygame.display.update()

            # aguardar entrada do jogador
            letter = None
            while letter is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print('Thanks for playing!')
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print('Thanks for playing!')
                            pygame.quit()
                            sys.exit()
                        elif event.unicode.isalpha():
                            letter = event.unicode.upper()

            if (self.player_turn == '1' and letter not in PLAYER_1_PITS) or (
                self.player_turn == '2' and letter not in PLAYER_2_PITS
            ):
                textj1 = fonte.render('Please pick a letter on your side of the board.', True, cor_texto)
                tela.blit(textj1, (1250, 436))
                pygame.display.update()
                continue

            if board.get(letter) == 0:
                print('Please pick a non-empty pit.')
                continue  # pedir mais uma jogada caso o jogador tenha clicado em uma casa vazia

            return letter
        
    def makeMove(self, board, pit):

        stonesToSow = board[pit]  # pegar o numero de pedras
        board[pit] = 0  # esvaziar o buraco selecionado

        while stonesToSow > 0:
            pit = NEXT_PIT[pit]
            if (self.player_turn == '1' and pit == '2') or (
                    self.player_turn == '2' and pit == '1'):
                continue
            board[pit] += 1
            stonesToSow -= 1

        if (pit == self.player_turn == '1') or (pit == self.player_turn == '2'):
            return self.player_turn

        # aplicação da regra da casa oposta

        if self.player_turn == '1' and pit in PLAYER_1_PITS and board[pit] == 1:
            oppositePit = OPPOSITE_PIT[pit]
            if board[oppositePit] > 0:
                board['1'] += board[oppositePit] + 1
                board[oppositePit] = 0
                board[pit] = 0
        elif self.player_turn == '2' and pit in PLAYER_2_PITS and board[pit] == 1:
            oppositePit = OPPOSITE_PIT[pit]
            if board[oppositePit] > 0:
                board['2'] += board[oppositePit] + 1
                board[oppositePit] = 0
                board[pit] = 0


        if self.player_turn == '1':
            return '2'
        elif self.player_turn == '2':
            return '1'
        
    def checkForWinner(self, board):  # checar o vencedor

        player1Total = board['A'] + board['B'] + board['C']
        player1Total += board['D'] + board['E'] + board['F']
        player2Total = board['G'] + board['H'] + board['I']
        player2Total += board['J'] + board['K'] + board['L']

        if player1Total == 0:
            board['2'] += player2Total
            for pit in PLAYER_2_PITS:
                board[pit] = 0
        elif player2Total == 0:
            board['1'] += player1Total
            for pit in PLAYER_1_PITS:
                board[pit] = 0
        else:
            return 'no winner'

        if board['1'] > board['2']:  # determinação do resultado
            return '1'
        elif board['2'] > board['1']:
            return '2'
        else:
            return 'tie'
    
class MancalaGame:


    def __init__(self):
        self.state = State()
        pygame.display.set_caption("Mancala Game")
        self.tela = pygame.display.set_mode((1400, 788))

        #self.clock = pygame.time.Clock()
        self.running = True

        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            self.tela.fill((255, 255, 255))
            pygame.display.flip()

            #self.clock.tick(60)

        

    def main(self):
        gameBoard = State().getNewBoard()
        
        running = True

        while running:  # correr a jogada de algum jogador
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
            
            self.tela.fill((255, 255, 255))
            pygame.display.flip()        
            State().displayBoard(gameBoard)
            playerMove = State().askForPlayerMove(gameBoard)

            self.player_turn = State().makeMove(gameBoard, playerMove)

            # testar se o jogo ja acabou e declarar o vencedor

            winner = State().checkForWinner(gameBoard)
            if winner == '1':
                tabuleiro_img = pygame.image.load("winner1.png")
                tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
                tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
                tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
                pygame.display.flip()
                running = False
                
            elif winner == '2':  # empate
                tabuleiro_img = pygame.image.load("winner2.png")
                tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
                tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
                tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
                pygame.display.flip()
                running = False
                        
            elif winner == 'tie':  # empate
                tabuleiro_img = pygame.image.load("tie.png")
                tabuleiro_x = (largura - tabuleiro_img.get_width()) // 2
                tabuleiro_y = (altura - tabuleiro_img.get_height()) // 2
                tela.blit(tabuleiro_img, (tabuleiro_x, tabuleiro_y))
                pygame.display.flip()
                running = False
    
if __name__ == '__main__':
    game = MancalaGame()
    game.main()


def evaluate(stoneAmounts):
    for i in range(7, 14):
        player1stones += stoneAmounts[i]
    for i in range(0, 7):
        player2stones += stoneAmounts[i]
    return player1stones - player2stones

def getPossibleMoves(tabuleiro, playerTurn):
    possibleMoves = []
    if playerTurn == "1":
        for i in range(8, 14):
            if tabuleiro[i] != 0:
                possibleMoves.append(PLAYER_1_PITS(i-8))
    if playerTurn == "2":
        for i in range(6):
            if tabuleiro[i] != 0:
                possibleMoves.append(PLAYER_2_PITS(i))
        
    return possibleMoves

def minimax(board, depth, max_player):
    if depth == 0 or State().checkForWinner(board):
        return evaluate(board)
    
    if max_player:
        max_eval = float('-inf')
        for move in getPossibleMoves(board):
            new_board = State().makeMove(board, move)
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in getPossibleMoves(board):
            new_board = State().makeMove(board, move)
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


''' def __init__(self):
        self.state = State(State.getNewBoard(), '1')'''
