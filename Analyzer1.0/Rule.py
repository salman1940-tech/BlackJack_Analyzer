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
# Hands_list:
# Dealer_list:
# operator: 
# ------------------output data after comparation of hand and dealer------------
# operation_list:
# event: "Tie", "Hands_Win", "Dealer_Win", "Continue", "Terminate"
def rule(Hands_list, Dealer_list, pre_operations, operator, debug = False):

	# extimate the compare result of hand cards and dealer, event
	if ( hard_value(Hands_list) > 21):
	# hand boom!
		event = "Dealer_Win"
		if (debug):
			print("lose rule 1 active!")
			print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
	elif ( hard_value(Dealer_list) > 21):
	# dealer boom!
		event = "Hands_Win"
		if (debug):
			print("win rule 1 active!")
			print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
	else:

		if ( operator == "hand"):
			if ( len(Hands_list) < 5):
			# continue as will, when hand playing
				event = "Continue"
			else:
				if (debug):
					print("Terminate condition detected")
				event = "Terminate"
		else:

			if ( soft_value(Dealer_list) < 17 ):
				event = "Continue"
			else:

				if ( (len(Hands_list) == 2) and (soft_value(Hands_list) == 21) ):	# blackjack 21
					hands_score = 5
				elif ( (len(Hands_list) == 5) and (soft_value(Hands_list) == 21) ):	# five dragon 21
					hands_score = 4
				elif ( (len(Hands_list) == 5) and (soft_value(Hands_list) < 21) ):	# five dragon
					hands_score = 3
				elif ( soft_value(Hands_list) == 21 ):								# normal 21
					hands_score = 2
				else:																# other cases
					hands_score = 1

				if ( (len(Dealer_list) == 2) and (soft_value(Dealer_list) == 21) ):		# blackjack 21
					dealer_score = 5
				elif ( (len(Dealer_list) == 5) and (soft_value(Dealer_list) == 21) ):	# five dragon 21
					dealer_score = 4
				elif ( (len(Dealer_list) == 5) and (soft_value(Dealer_list) < 21) ):	# five dragon
					dealer_score = 3
				elif ( soft_value(Dealer_list) == 21 ):									# normal 21
					dealer_score = 2
				else:
					dealer_score = 1

				if (hands_score > dealer_score):
					event = "Hands_Win"
					if (debug):
						print("win rule 2 active!")
						print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
				elif (hands_score < dealer_score):
					event = "Dealer_Win"
					if (debug):
						print("lose rule 2 active!")
						print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
				else:

					if (hands_score > 1):
						event = "Tie"
						if (debug):
							print("tie rule 1 active!")
							print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
					else:

						if ( soft_value(Hands_list) > soft_value(Dealer_list) ):
							event = "Hands_Win"
							if (debug):
								print("rule 3 active!")
								print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
						elif ( soft_value(Dealer_list) > soft_value(Hands_list) ):
							event = "Dealer_Win"
							if (debug):
								print("lose rule 3 active!")
								print("hands: ", Hands_list, "\tdealer: ", Dealer_list)
						else:
							event = "Tie"
							if (debug):
								print("tie rule 2 active!")
								print("hands: ", Hands_list, "\tdealer: ", Dealer_list)

	# provide strategy for operator, operation_list
	operation_list = []
	if ( operator == "dealer"):
		operation_list.append("Hit")
		operation_list.append("Stand")
	else:

		# insurance
		if ( (len(pre_operations) == 0) and (Dealer_list[0] == 1) and (len(Hands_list) == 2) and (len(Dealer_list) == 1) ):
			operation_list.append("Buy_Insurance")
			operation_list.append("No_Insurance")
			return(operation_list, event)

		# first round operations
		if ( len(Hands_list) == 2 ):
			operation_list.append("Double")
		if ( (len(Hands_list) == 2) and (Hands_list[0] == Hands_list[1]) and (not ("Split" in pre_operations))):
			operation_list.append("Split")

		# others
		if ( not ("Double" in pre_operations) ):
			operation_list.append("Stand")
			operation_list.append("Hit")

	return(operation_list, event)
