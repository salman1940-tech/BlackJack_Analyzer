def soft_value(cards_list):
	if (not (1 in cards_list)):
		re = sum(cards_list)
	else:
		tmp = sum(cards_list)
		if (tmp <= 11):
			re = tmp + 10
		else:
			re = tmp
	return(re)

def hard_value(cards_list):
	re = sum(cards_list)
	return(re)

# ------------------input data for defination of game rule----------------------
# Hands_list: List of Hand cards value
# Dealer_list: List of Dealer's cards value
# operator: Who is operator now, "dealer" of "hand"
# ------------------output data after comparation of hand and dealer------------
# operation_list: Operations can be used in next step
# event: "Tie", "Hands_Win", "Dealer_Win", "Continue", "Terminate"
# profit: The ratio of earning to stake
def rule(Hands_list, Dealer_list, pre_operations, operator, debug = False):

	Amend_facotr = 0.95
	profit = 0.0

	# assign hand cards and dealer cards a score
	if ( (len(Hands_list) == 2) and (soft_value(Hands_list) == 21) ):   # blackjack 21
		hands_score = 5
	elif ( (len(Hands_list) == 5) and (soft_value(Hands_list) == 21) ): # five dragon 21
		hands_score = 4
	elif ( (len(Hands_list) == 5) and (soft_value(Hands_list) < 21) ):  # five dragon
		hands_score = 3
	elif ( soft_value(Hands_list) == 21 ):                              # normal 21
		hands_score = 2
	elif ( soft_value(Hands_list) < 21):								# other cases
		hands_score = 1
	else:																# boom!
		hands_score = 0

	if ( (len(Dealer_list) == 2) and (soft_value(Dealer_list) == 21) ):     # blackjack 21
		dealer_score = 5
	elif ( (len(Dealer_list) == 5) and (soft_value(Dealer_list) == 21) ):   # five dragon 21
		dealer_score = 4
	elif ( (len(Dealer_list) == 5) and (soft_value(Dealer_list) < 21) ):    # five dragon
		dealer_score = 3
	elif ( soft_value(Dealer_list) == 21 ):                                 # normal 21
		dealer_score = 2
	elif ( soft_value(Dealer_list) < 21 ):									# other cases
		dealer_score = 1
	else:																	# boom!
		dealer_score = 0

	if (debug):
		print("hands score: ", hands_score, "\tdealer score: ", dealer_score)

	# estimate the compare result
	if ( hands_score == 0 ):
	# Hand boom!
		event = "Dealer_Win"
		profit = -1.0
		if (debug):
			print("lose rule 1 active! Hands Boom!")
			print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

	elif ( dealer_score == 0 ):
	# Dealer boom!
		event = "Hands_Win"
		if ( hands_score >= 3):
			# rule that: blackjack 21 traet as normal 21 for a split cards
			#if ((hands_score == 5) and ("Split" in pre_operations)):
			#	profit = 1.0
			#else:
			#	profit = 1.5
			profit = 1.5
		elif ( (len(Hands_list) == 3) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) ):	# three of kings, 1.5 times stake
			profit = 1.5
		elif ( (len(Hands_list) == 4) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) and (Hands_list[2] == Hands_list[3]) ):  # four of kings, 2.0 times stake
			profit = 2.0
		else:
			profit = 1.0

		if (debug):
			print("win rule 1 active! Dealer Boom!")
			print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

	else:

		if ( operator == "hand"):
			if ( len(Hands_list) < 5):
			# It can always continue when hand playing
				event = "Continue"
			else:
				event = "Terminate"

		else:

			if ( (soft_value(Dealer_list) < 17) and (len(Dealer_list) < 5) ):
				event = "Continue"
			else:

				if (hands_score > dealer_score):
					event = "Hands_Win"
					if ( hands_score >= 3):
						# rule that: blackjack 21 traet as normal 21 for a split cards
						#if ((hands_score == 5) and ("Split" in pre_operations)):
						#	profit = 1.0
						#else:
						#	profit = 1.5
						profit = 1.5
					elif ( (len(Hands_list) == 3) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) ):  # three of kings, 1.5 times stake
						profit = 1.5
					elif ( (len(Hands_list) == 4) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) and (Hands_list[2] == Hands_list[3]) ):  # four of kings, 2.0 times stake
						profit = 2.0
					else:
						profit = 1.0

					if (debug):
						print("win rule 2 active! Hands score higher than Dealer")
						print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

				elif (hands_score < dealer_score):
					event = "Dealer_Win"
					profit = -1.0

					if (debug):
						print("lose rule 2 active! Hands score lower than Dealer")
						print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

				else:

					if (hands_score > 1):
						event = "Tie"
						if ( (len(Hands_list) == 3) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) ):  # three of kings, 1.5 times stake
							profit = 1.5
						elif ( (len(Hands_list) == 4) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) and (Hands_list[2] == Hands_list[3]) ):  # four of kings, 2.0 times stake
							profit = 2.0
						else:
							profit = 0.0

						if (debug):
							print("tie rule 1 active!")
							print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

					else:

						if ( soft_value(Hands_list) > soft_value(Dealer_list) ):
							event = "Hands_Win"
							if ( (len(Hands_list) == 3) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) ):  # three of kings, 1.5 times stake
								profit = 1.5
							elif ( (len(Hands_list) == 4) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) and (Hands_list[2] == Hands_list[3]) ):  # four of kings, 2.0 times stake
								profit = 2.0
							else:
								profit = 1.0

							if (debug):
								print("win rule 2 active! Hands value higher than Dealer")
								print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

						elif ( soft_value(Hands_list) < soft_value(Dealer_list) ):
							event = "Dealer_Win"
							profit = -1.0

							if (debug):
								print("lose rule 2 active! Hands value lower than Dealer")
								print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

						else:

							if ( (len(Hands_list) == 3) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) ):  # three of kings, 1.5 times stake
								event = "Hands_Win"
								profit = 1.5
							elif ( (len(Hands_list) == 4) and (Hands_list[0] == Hands_list[1]) and (Hands_list[1] == Hands_list[2]) and (Hands_list[2] == Hands_list[3]) ):  # four of kings, 2.0 times stake
								event = "Hands_Win"
								profit = 2.0
							else:
								event = "Tie"
								profit = 0.0
								if (debug):
									print("tie rule 2 active!")
									print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

	# provide strategies for operator, operation_list
	operation_list = []
	if ( operator == "dealer"):
		operation_list.append("Hit")
		operation_list.append("Stand")
	else:

		# insurance
		if ( (len(pre_operations) == 0) and (Dealer_list[0] == 1) and (len(Hands_list) == 2) and (len(Dealer_list) == 1) ):
			operation_list.append("Buy_Insurance")
			operation_list.append("No_Insurance")
			return(operation_list, event, profit)

		# operation only avaliable in first round
		if ( (len(Hands_list) == 2) ):
			operation_list.append("Double")
		if ( (len(Hands_list) == 2) and (Hands_list[0] == Hands_list[1]) and (not ("Split" in pre_operations))):
			operation_list.append("Split")

		# others
		if ( not ("Double" in pre_operations) ):
			operation_list.append("Stand")
			operation_list.append("Hit")

	if (profit > 0):
		profit *= Amend_facotr
	return(operation_list, event, profit)
