#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "suvasama"
__date__ = "$Jan 11, 2018 11:31:04 AM$"

# The program implements a version of the rock-paper-scissors game in which the 
# player plays againts artificial intelligence (AI or machine)

# Machine player adopts the following (simple) strategy:
# In the first round, play "r" with prob 0.296, "p" with prob 0.354 and "s" 
# with prob 0.35
# Keep track on the player's moves from the first ten rounds
# In the second round, assume that the player does not play the same strategy 
# than in the previous round. Assign probability 1/2 to each strategy and play 
# the best response.
# Starting from the third round, assume that the player is more likely to play 
# the same strategy in the future if they lost this round and less likely to
# play it if they lost or broke even
# After ten rounds, start playing each action with equal probability


import random

# AI: machine player
class RPSai: 
    def __init__(self):
        self.moves = ["r", "p", "s"];
        self.weights = [0.296, 0.354, 0.35];
        self.firstMove = [];
        self.alpha = 1/8;       # parameter that determines the weight of 
                                # previous action that ai used to adjust its 
                                # expectation of the player's strategy
        
    def memory(self, playersMove, aisMove,i):
        if i == 0:
            self.firstMove.append(playersMove)
        if playersMove == "r":
            if aisMove == "s":
                    self.weights[0] = max(min(self.weights[0] - self.alpha/2,1),0); 
                    self.weights[1] = max(min(self.weights[1] + self.alpha,1),0);
                    self.weights[2] = max(min(self.weights[2] - self.alpha/2,1),0);
            else:
                    self.weights[0] = max(min(self.weights[0] + self.alpha/2,1),0); 
                    self.weights[1] = max(min(self.weights[1] - self.alpha,1),0);
                    self.weights[2] = max(min(self.weights[2] + self.alpha/2,1),0);
        elif playersMove == "p":
            if aisMove == "r":
                    self.weights[0] = max(min(self.weights[0] - self.alpha/2,1),0);
                    self.weights[1] = max(min(self.weights[1] - self.alpha/2,1),0);
                    self.weights[2] = max(min(self.weights[2] + self.alpha,1),0);
            else:
                    self.weights[0] = max(min(self.weights[0] + self.alpha/2,1),0); 
                    self.weights[1] = max(min(self.weights[1] + self.alpha/2,1),0);
                    self.weights[2] = max(min(self.weights[2] - self.alpha,1),0);
        else:
            if aisMove == "p":
                    self.weights[0] = max(min(self.weights[0] + self.alpha,1),0); 
                    self.weights[1] = max(min(self.weights[1] - self.alpha/2,1),0);
                    self.weights[2] = max(min(self.weights[2] - self.alpha/2,1),0);
            else:
                    self.weights[0] = max(min(self.weights[0] - self.alpha,1),0); 
                    self.weights[1] = max(min(self.weights[1] + self.alpha/2,1),0);
                    self.weights[2] = max(min(self.weights[2] + self.alpha/2,1),0);
    
    # AI's move
    def makeMove(self,i):
        if i == 0:
            if self.firstMove == "r":
                return random.choice(['r', 's'])
            elif self.firstMove == "p":
                return random.choice(['r', 'p'])
            else:
                return random.choice(['r', 'p'])
        elif i < 10:
            # Following code generates a random decision using the weights 
            # computed by the previous function
            j = random.random();
            if j <= self.weights[0]:
                j = 0;
            elif j <= self.weights[0] + self.weights[1]:
                j = 1;
            else:
                j = 2;
        else:
            j = random.randint(0,len(self.moves) - 1)
        return self.moves[j];

# REFEREE: determines the winner
class RPSReferee:
    def __init__(self):
        self.aiWins = 0;
        self.plWins = 0;
    
    def whosWinner(self, playersMove, aisMove):
        if playersMove == aisMove:
            print "Break even!"
        elif (
        (playersMove == "r" and aisMove == "s") or \
        (playersMove == "p" and aisMove == "r") or \
        (playersMove == "s" and aisMove == "p")
        ):
            print "You win!"
            self.plWins = self.plWins + 1;
        else:
            print "Machine player wins!"
            self.aiWins = self.aiWins + 1;
            
    def printStats(self):
        print "\nStatistics:\nYou won " + str(self.plWins) + " times\n" \
            "Machine player won " + str(self.aiWins) + " times"
        
def notaMove(playersMove):
    moves = ["r", "p", "s"]
    if playersMove not in moves:
        return True;
    return False;
        
ai = RPSai();
referee = RPSReferee();

rounds = input("How many rounds? ");

i = 0;
while i < rounds:

    # Ask Player make a move
    playersMove = raw_input("Make a move (r, p or s): ")
    if notaMove(playersMove):
        continue;

    # Machine player makes a move
    aisMove = ai.makeMove(i)
    print "Machine player's move: " + aisMove
    ai.memory(playersMove, aisMove,i)
    referee.whosWinner(playersMove, aisMove)

    # Counter for rounds that have been played
    i += 1;

referee.printStats()