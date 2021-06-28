from random import shuffle, randint

class Helper:
	def __init__(self):
		self.helo = True

	def print_help(self):
		return "hello"

class Card:

	def __init__(self, newColour, newAction, isActive = False, newOriginal = None):
		self.colour = newColour
		self.action = newAction
		self.isActive = isActive
		self.orignalValue = newOriginal

	def setColour(self, newColour):
		self.colour = newColour

	def setAction(self, newAction):
		self.action = newAction

	def getColour(self):
		return self.colour

	def getAction(self):
		return self.action

	def setActive(self, newActive):
		self.isActive = newActive

	def getActive(self):
		return self.isActive

	def getOriginalValue(self):
		return self.orignalValue

	def isCardPlus(self, no):
		if self.action == 'plus ' + str(no):
			return True
		else: 
			return False

	def isBlackCard(self):
		if self.colour == 'black':
			return True
		else:
			return False

	def isSkipCard(self):
		if self.action == 'skip':
			return True
		else:
			return False

	def isReverseCard(self):
		if self.action == 'reverse':
			return True
		else:
			return False

	def __str__(self):
		cardStatus = "Card: " + self.colour + " " + self.action
		return cardStatus

class Player:
	def __init__(self, isHuman = False):
		self.name = ""
		self.isHuman = isHuman
		self.hand = []
		self.unoStatus = False

	def __str__(self):
		if self.getHumanStatus():
			playerDetails = self.name + " is a human player"
		else:
			playerDetails = self.name + " is NOT a human player"
		return playerDetails

	def setName(self):
		self.name = input("Player - Enter your name? ")

	def getName(self):
		return self.name

	def getPlayerHand(self):
		return self.hand

	def getHumanStatus(self):
		if self.isHuman:
			return True
		else:
			return False

	def setUnoStatus(self, newStatus):
		self.unoStatus = newStatus

	def getUnoStatus(self):
		return self.unoStatus

	def dealHand(self, deck):
		for i in range(7):
			self.pickCardFromDeck(deck)

	def pickCardFromDeck(self, deck):
		self.hand.append(deck.pop())

	def picksUpCards(self, game):

		counter = game.getPickUpCounter()
		if counter == 0:
			counter = 1

		if counter > len(game.getDeck()):
			game.reshuffleDiscardPile()

		if counter > len(game.getDeck()):
			counter = len(game.getDeck())
		for i in range(counter):
			self.hand.append(game.getDeck().pop())
			self.setUnoStatus(False)

		print(self.getName() + " picks up " + str(counter) + " card(s) from the deck.")

	def showPlayerHand(self, counter):
		print("\n")
		print(self.getName() + ". Here is your hand.", end="\n")

		if self.getUnoStatus():
			print(self.getName() + " is on UNO")
		if counter == 0:
			counter = 1

		for i in range(len(self.hand)):
			print(str(i + 1) + " "+str(self.hand[i]))
		finalPos = len(self.hand) + 1
		print(str(finalPos) + " " + "Pick " + str(counter) + " Card(s) from deck")

		if len(self.getPlayerHand()) == 2 and self.getUnoStatus() == False:
			unoPos = len(self.getPlayerHand()) + 2
			print(str(unoPos) + " Annouce UNO!")
		print("\n")

	def getPlayersChoice(self, game):
		
		validChoice = False

		if len(self.hand) == 2:
			choiceLimit = len(self.getPlayerHand()) + 2
		else:
			choiceLimit = len(self.getPlayerHand()) + 1

		if self.getHumanStatus():
			self.showPlayerHand(game.getPickUpCounter())

		while(validChoice == False):
			try:
				if self.getHumanStatus():
					choice = int(input(self.getName() + ". Please select an option: "))
				else:
					if self.getUnoStatus() == False and len(self.getPlayerHand()) == 2:
						choice = choiceLimit
					else:
						choice = randint(1, choiceLimit)
				validChoice = True
			except ValueError:
				print("Only integers are allowed")
		return choice

	def playsCard(self, choice, game): #Player's Choice is (i - 1)
		isValid = False
		playingCard = self.getPlayerHand()[choice - 1]
		isValid = game.checkIsValidMove(playingCard)
		if isValid:
			playingCard = self.getPlayerHand().pop(choice - 1)
			game.setCardInPlay(playingCard)
			game.addToDiscardPile(playingCard)
			print(self.getName() + " plays " + str(playingCard))
			if playingCard.isBlackCard():
				colorInput = self.selectColor(game)
				card = Card(colorInput, playingCard.getAction(), True)
				game.setCardInPlay(card)
		else:
			if self.getHumanStatus():
				print(self.getName() + ". This card cannot be played here. Please choose another.")

		return isValid

	def selectColor(self, game):
		isValid = False
		if self.isHuman:
			print("\n")
			for i in range(len(game.colors)):
				print(str(i + 1) + " - " + game.colors[i])

		while(isValid == False):
			if self.isHuman:
				colourInput = int(input(self.name + " - Please select a colour: "))
				isValid = game.checkPlayerInput(self.name, colourInput, len(game.colors))
			else:
				colourInput = randint(0, len(game.colors) - 1)
				isValid = True

		chosenColour = game.colors[colourInput - 1]
		print(self.getName() + " changes the colour to " + chosenColour)
		return chosenColour

class Game:
	def __init__(self):
		self.colors = ["green", "red", "blue", "yellow"]
		self.speciaCards = ["skip", "reverse", "plus 2"]
		self.blackCards = ["plus 4", "change colour"]
		self.deck = self.createDeck()
		self.playerList = self.createPlayers()
		self.winner = None
		self.cardInPlay = None
		self.isReverse = False
		self.isSkip = False
		self.pickUpCounter = 0
		self.discardPile = ["", ""]
		self.discardPile.clear()

	def createDeck(self):
		deck = [Card("black", "plus 4"), Card("black", "change colour")]
		deck.clear()
	
		for i in range(4):
			for card in self.blackCards:
				card = Card("black", card, True, card)
				deck.append(card)

		for color in self.colors:
		
			Card(color, "0") #1 set of 0's

			for i in range(2): #2 sets of coloured card from 1 to 9
				for j in range(1, 10):
					card = Card(color, str(j))
					deck.append(card)
				for card in self.speciaCards: #2 sets of special colored cards
					card = Card(color, card, True)
					deck.append(card)

		shuffle(deck)
		return deck

	def createPlayers(self):

		isValidNoOfPlayers = False
		while (isValidNoOfPlayers == False):
			try:
				noOfPlayers = int(input("How many players are in this game? "))
				if noOfPlayers < 2:
					raise ValueError("At least 2 players are required to game this name.")
				elif noOfPlayers > 10:
					raise ValueError("Only a maximum of 10 players can play this game")
				else:
					isValidNoOfPlayers = True
			except ValueError:
				print("Incorrect Input. Please enter a correct value")
				print("Please try again")


		for i in range(0, noOfPlayers):
			if i == 0:
				player = Player(True)
				playerList = [player]
			else:
				player = Player()
				playerList.append(player)

			player.setName()
			player.dealHand(self.deck)

		return playerList

	def setDeck(self, newDeck):
		self.deck = newDeck

	def getDeck(self):
		return self.deck

	def addToDiscardPile(self, newCard):
		newCard.setActive(True)
		self.discardPile.append(newCard)

	def getDiscardPile(self):
		return self.discardPile

	def resetDiscardPile(self):
		self.discardPile.clear()

	def getPlayerList(self):
		return self.playerList

	def checkPlayerInput(self, name, playerInput, limit):
		if playerInput > limit or playerInput < 1:
			print("Please play a valid option.")
			return False
		else:
			return True

	def setCardInPlay(self, newCard):
		self.cardInPlay = newCard
		#self.setDiscardPile(newCard)

	def getCardInPlay(self):
		return self.cardInPlay

	def displayCardInPlay(self):
		print("Card in Play:", self.cardInPlay, end="\n")

	def setPickUpCounter(self, card, unoCounter = False):
		if card.isCardPlus(2) and card.getActive():
			card.setActive(False)
			self.pickUpCounter += 2 
		elif card.isCardPlus(4) and card.getActive(): 
			card.setActive(False)
			self.pickUpCounter += 4
		elif unoCounter:
			self.pickUpCounter = 2

	def getPickUpCounter(self):
		return self.pickUpCounter

	def resetPickCounter(self):
		self.pickUpCounter = 0

	def checkIsValidMove(self, playerCard):
		isValid = False
		if self.getPickUpCounter() >=4 and self.getCardInPlay().isCardPlus(4):
			if playerCard.isCardPlus(4):
				isValid = True
		elif self.getPickUpCounter() >=2 and self.getCardInPlay().isCardPlus(2):
			if playerCard.isCardPlus(2) or playerCard.isCardPlus(4):
				isValid = True
		elif self.getPickUpCounter() == 0:
			if playerCard.isBlackCard():
				isValid = True
			elif self.getCardInPlay().getColour() == playerCard.getColour():
				isValid = True
			elif self.getCardInPlay().getAction() == playerCard.getAction():
				isValid =  True
		return isValid

	def checkWinner(self, player):
		if len(player.getPlayerHand()) == 0:
			if player.getUnoStatus():
				self.winner = player
			else:
				print(player.getName() + " has failed to declared UNO. Therefore " + player.getName() + "must pick up two cards.")
				uno.setPickUpCounter(uno.getCardInPlay(), True)
				player.picksUpCards(uno)

	def getWinner(self):
		return self.winner

	def setUpStartingCard(self):
		isValid = False
		while(isValid == False):
			self.setCardInPlay(self.deck.pop())
			if self.getCardInPlay().isBlackCard() == False:
				if self.getCardInPlay().isReverseCard() == False:
					if self.getCardInPlay().isSkipCard() == False:
						if self.getCardInPlay().isCardPlus(2) == False:
							isValid = True

	def checkReverse(self, card):
		if card.getAction() == 'reverse' and card.getActive():
			card.setActive(False)
			if self.isReverse:
				self.isReverse = False
			else:
				self.isReverse = True

			return card

	def getIsReverse(self):
		return self.isReverse

	def checkIsSkip(self, card):
		if card.getAction() == 'skip' and card.getActive():
			card.setActive(False)
			return True
		else:
			return False

	def reshuffleDiscardPile(self):
		shuffle(self.getDiscardPile())
		self.setDeck(self.getDiscardPile().copy())
		print("The deck as been re-shuffled")
		print("\n")
		self.resetDiscardPile()

uno = Game()
playerPosition = 0
uno.setUpStartingCard()
currentPlayer = uno.getPlayerList()[playerPosition]

while(uno.getWinner() == None):
	uno.displayCardInPlay()
	nextTurn = False
	print("\n")
	if uno.checkIsSkip(uno.getCardInPlay()):
		print(currentPlayer.getName() + " is skipped!")
	else:
		while(nextTurn == False):
			try:
				playerChoice = currentPlayer.getPlayersChoice(uno)
				#Picks up Card
				if playerChoice == len(currentPlayer.getPlayerHand()) + 1:
					currentPlayer.picksUpCards(uno)
					uno.resetPickCounter()
					nextTurn = True
				#Set UNO Status
				elif playerChoice == len(currentPlayer.getPlayerHand()) + 2: 
					currentPlayer.setUnoStatus(True) 
					print(currentPlayer.getName() + " has declared UNO!")
				else:
					nextTurn = currentPlayer.playsCard(playerChoice, uno)
			except IndexError:
					print(currentPlayer.getName() + " - Please select a option in range")

	uno.checkWinner(currentPlayer)
	uno.checkReverse(uno.getCardInPlay())
	uno.setPickUpCounter(uno.getCardInPlay())

	if uno.getIsReverse():
		if playerPosition == 0:
			playerPosition = len(uno.getPlayerList()) - 1
		else:
			playerPosition -= 1
	else:
		if playerPosition == len(uno.getPlayerList()) - 1:
			playerPosition = 0
		else:
			playerPosition += 1
	currentPlayer = uno.getPlayerList()[playerPosition]

print(uno.getWinner().getName() + " WINS!")