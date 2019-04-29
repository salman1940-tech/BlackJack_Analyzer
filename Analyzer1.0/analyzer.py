from Rule import rule
import datetime

class BJ_analyzer:

	decks = 1;
	Cards = {}
	Cards_Amount = 0
	Dealer = []
	Hands = []

	pre_operations = []

	def __init__(self, decks = 1):

		for ii in range(9):
			i = ii + 1
			self.Cards[i] = 4 * decks
			self.Cards_Amount += 4 * decks
		self.Cards[10] = 16 * decks
		self.Cards_Amount += 16 * decks

		self.decks = decks


	def iter_hands(self, hands_list = []):
	#	print("pre_operations: ", self.pre_operations)

		operation_list, event = rule(hands_list, self.Dealer, self.pre_operations, "hand")
		Equityedge = {}		# dictionary for store win rate of each strategy

		if ( (event != "Continue") and (event != "Terminate") ):
			key_name = "Branch_End"
			if ( event == "Dealer_Win" ):
				Equityedge[key_name] = -1.0
			if ( event == "Hands_Win" ):
				Equityedge[key_name] = 1.0
			if ( event == "Tie" ):
				Equityedge[key_name] = 0
			return(Equityedge)
		elif (event == "Terminate"):
			win_rate = self.iter_dealer(hands_list.copy())
			Equityedge["Terminate"] = 1.0 * (2 * win_rate - 1)
			return(Equityedge)


		if ("Buy_Insurance" in operation_list):
		# buy insurance branch
			profit = -0.5
			self.pre_operations.append('Buy_Insurance')
			# when dealer card is BlackJack, then receive double insurance compensation.
			ratio = self.Cards[10] / self.Cards_Amount
			profit += ratio * 1.0
			# or dealer card is not BlackJack
			# search through cards without 10 for first hitting of dealer, then enter next iteration of hands
			next_eq1 = {}
			for aa1 in range(9):
				a1 = aa1 + 1
				if (self.Cards[a1] > 0):
					ratio = self.Cards[a1] / self.Cards_Amount
					self.Dealer.append(a1)
					self.Cards_Amount -= 1
					# enter next iteration of hands
					eq_dict = self.iter_hands(hands_list.copy())
					opt_profit = -10
					for key in eq_dict:
						if (key in next_eq1):
							next_eq1[key] += eq_dict[key] * ratio
						else:
							next_eq1[key] = eq_dict[key] * ratio
						if (eq_dict[key] > opt_profit):
							opt_profit = eq_dict[key]
					profit += ratio * opt_profit

					self.Dealer = self.Dealer[:-1]
					self.Cards_Amount += 1

			# add win rate of Buy_Insurance to Equityedge dictionary
			Equityedge["Buy_Insurance"] = [profit, next_eq1]
			self.pre_operations = self.pre_operations[:-1]

		# no insurance branch
			profit = 0.0
			self.pre_operations.append('No_Insurance')

			next_eq2 = {}
			eq_dict = self.iter_hands(hands_list.copy())
			opt_profit = -10
			for key in eq_dict:
				next_eq2[key] = eq_dict[key] * ratio
				if (eq_dict[key] > opt_profit):
					opt_profit = eq_dict[key]
			profit = opt_profit

			# add win rate of No_Insurance to Equityedge dictionary
			Equityedge["No_Insurance"] = [profit, next_eq2]
			self.pre_operations = self.pre_operations[:-1]

		if ("Split" in operation_list):
		# split branch
			profit = 0.0
			self.pre_operations.append("Split")
			tmp_list1 = [hands_list[0]]
			tmp_list2 = [hands_list[1]]

#------------excat iteration code for this branch, but too waste time-------------
			for aa1 in range(10):
				a1 = aa1 + 1
				ratio1 = self.Cards[a1] / self.Cards_Amount

				if (self.Cards[a1] > 0):
					tmp_list1.append(a1)
					self.Cards[a1] -= 1
					self.Cards_Amount -= 1

					for aa2 in range(aa1, 10):
						a2 = aa2 + 1
						ratio2 = self.Cards[a2] / self.Cards_Amount
						if (aa2 == aa1):
							ratio2 /= 2

						if (self.Cards[a2] > 0):
							tmp_list2.append(a2)
							self.Cards[a2] -= 1
							self.Cards_Amount -= 1

							# entering next iteration for each heap of hand cards
							eq_dict1 = self.iter_hands(tmp_list1.copy())
							eq_dict2 = self.iter_hands(tmp_list2.copy())

							opt_profit1 = -10
							for key in eq_dict1:
								if (eq_dict1[key] > opt_profit1):
									opt_profit1 = eq_dict1[key]
							opt_profit2 = -10
							for key in eq_dict2:
								if (eq_dict2[key] > opt_profit2):
									opt_profit2 = eq_dict2[key]

							tmp_list2 = tmp_list2[:-1]
							self.Cards[a2] += 1
							self.Cards_Amount += 1

							profit += (opt_profit1 + opt_profit2) * ratio1 * ratio2

					tmp_list1 = tmp_list1[:-1]
					self.Cards[a1] += 1
					self.Cards_Amount += 1
#--------------------------------excat code end-----------------------------------
			"""
		# approximation that two heap of cards splited have the same win rate
			for aa1 in range(10):
				a1 = aa1 + 1
				ratio = self.Cards[a1] / self.Cards_Amount

				if (self.Cards[a1] > 0):
					tmp_list1.append(a1)
					self.Cards[a1] -= 1
					self.Cards_Amount -= 1

					# entering next iteration
					eq_dict = self.iter_hands(tmp_list1.copy())
					opt_profit = -10
					for key in eq_dict:
						if (eq_dict[key] > opt_profit):
							opt_profit = eq_dict[key]
					profit += opt_profit * ratio * 2.0

					tmp_list1 = tmp_list1[:-1]
					self.Cards[a1] += 1
					self.Cards_Amount += 1

		# approximation code end
			"""
			# add win rate of Split to Equityedge dictionary
			self.pre_operations = self.pre_operations[:-1]
			Equityedge["Split"] = profit

		if ("Double" in operation_list):
		#	print("operation: Double")
		# double branch
			profit = 0
			self.pre_operations.append("Double")
			# only hit one more card
			for aa1 in range(10):
				a1 = aa1 + 1
				ratio = self.Cards[a1] / self.Cards_Amount

				if (self.Cards[a1] > 0):
					hands_list.append(a1)
					self.Cards[a1] -= 1
					self.Cards_Amount -= 1
					# entering iteration of dealer
					win_rate = self.iter_dealer(hands_list.copy())
					profit += 2.0 * (2 * win_rate - 1) * ratio

#					print("new profit: ", 2.0 * (2 * win_rate - 1) * ratio)

					hands_list = hands_list[:-1]
					self.Cards[a1] += 1
					self.Cards_Amount += 1

			# add win rate of Double to Equityedge dictionary
			Equityedge["Double"] = profit
			self.pre_operations = self.pre_operations[:-1]

		if ("Hit" in operation_list):
		#	print("operation: Hit")
		# hitting branch
			profit = 0
			self.pre_operations.append('Hit')
			# hit one card then enter next iteration
			for aa1 in range(10):
				a1 = aa1 + 1
				ratio = self.Cards[a1] / self.Cards_Amount

				if (self.Cards[a1] > 0):
					hands_list.append(a1)
					self.Cards[a1] -= 1
					self.Cards_Amount -= 1
					# entering next iteration of hands
					eq_dict = self.iter_hands(hands_list.copy())
					opt_profit = -10
					for key in eq_dict:
						if (eq_dict[key] > opt_profit):
							opt_profit = eq_dict[key]
					profit += opt_profit * ratio

					hands_list = hands_list[:-1]
					self.Cards[a1] += 1
					self.Cards_Amount += 1

			Equityedge["Hit"] = profit
			self.pre_operations = self.pre_operations[:-1]

		if ( ("Stand" in operation_list) or (event == "Terminate") ):
		#	print("operation: Stand")
		# stop any operation
			profit = 0.0
			self.pre_operations.append("Stand")

			win_rate = self.iter_dealer(hands_list.copy())
			profit += (2 * win_rate - 1) * 1.0

			Equityedge["Stand"] = profit
			self.pre_operations = self.pre_operations[:-1]

	#	print("hand cards: ", hands_list, "\tEquityedge: ", Equityedge)
		return(Equityedge)

	def iter_dealer(self, hands_list, debug_ana = False):

		operation_list, event1 = rule(hands_list, self.Dealer, self.pre_operations, "dealer", debug = debug_ana)
		win_rate = 0

		if (event1 == "Continue"):
			for aa1 in range(10):
				a1 = aa1 + 1
				ratio1 = self.Cards[a1] / self.Cards_Amount

				if (self.Cards[a1] > 0):
					self.Dealer.append(a1)
					self.Cards[a1] -= 1
					self.Cards_Amount -= 1

					operation_list, event2 = rule(hands_list, self.Dealer, self.pre_operations, "dealer", debug = debug_ana)

					if (event2 == "Continue"):
						for aa2 in range(10):
							a2 = aa2 + 1
							ratio2 = self.Cards[a2] / self.Cards_Amount

							if (self.Cards[a2] > 0):
								self.Dealer.append(a2)
								self.Cards[a2] -= 1
								self.Cards_Amount -= 1

								operation_list, event3 = rule(hands_list, self.Dealer, self.pre_operations, "dealer", debug = debug_ana)

								if (event3 == "Continue"):
									for aa3 in range(10):
										a3 = aa3 + 1
										ratio3 = self.Cards[a3] / self.Cards_Amount

										if (self.Cards[a3] > 0):
											self.Dealer.append(a3)
											self.Cards[a3] -= 1
											self.Cards_Amount -= 1

											operation_list, event4 = rule(hands_list, self.Dealer, self.pre_operations, "dealer", debug = debug_ana)

											if (event4 == "Continue"):
												for aa4 in range(10):
													a4 = aa4 + 1
													ratio4 = self.Cards[a4] / self.Cards_Amount

													if (self.Cards[a4] > 0):
														self.Dealer.append(a4)
														self.Cards[a4] -= 1
														self.Cards_Amount -= 1

														operation_list, event5 = rule(hands_list, self.Dealer, self.pre_operations, "dealer", debug = debug_ana)

														if (event5 == "Tie"):
															win_rate += 0.5 * ratio1 * ratio2 * ratio3 * ratio4
														if (event5 == "Hands_Win"):
															win_rate += 1.0 * ratio1 * ratio2 * ratio3 * ratio4

														self.Dealer = self.Dealer[:-1]
														self.Cards[a4] += 1
														self.Cards_Amount += 1

											if (event4 == "Tie"):
												win_rate += 0.5 * ratio1 * ratio2 * ratio3
											if (event4 == "Hands_Win"):
												win_rate += 1.0 * ratio1 * ratio2 * ratio3

											self.Dealer = self.Dealer[:-1]
											self.Cards[a3] += 1
											self.Cards_Amount += 1

								if (event3 == "Tie"):
									win_rate += 0.5 * ratio1 * ratio2
								if (event3 == "Hands_Win"):
									win_rate += 1.0 * ratio1 * ratio2

								self.Dealer = self.Dealer[:-1]
								self.Cards[a2] += 1
								self.Cards_Amount += 1

					if (event2 == "Tie"):
						win_rate += 0.5 * ratio1
					if (event2 == "Hands_Win"):
						win_rate += 1.0 * ratio1

					self.Dealer = self.Dealer[:-1]
					self.Cards[a1] += 1
					self.Cards_Amount += 1

		if (event1 == "Tie"):
			win_rate = 0.5

		if (event1 == "Dealer_Win"):
			win_rate = 0.0

		if (event1 == "Hands_Win"):
			win_rate = 1.0

		if (debug_ana):
			print("dealer: ", self.Dealer, "\thands: ", hands_list, "\twin rate: ", win_rate)

		return(win_rate)

	def clear(self):
		self.Cards = {}
		self.Cards_Amount = 0
		self.Dealer = []
		self.Hands = []
		self.pre_operations = []

		for ii in range(9):
			i = ii + 1
			self.Cards[i] = 4 * self.decks
			self.Cards_Amount += 4 * self.decks
		self.Cards[10] = 16 * self.decks
		self.Cards_Amount += 16 * self.decks

	def hand_push(self, card_value):
		if (self.Cards[card_value] > 0):
			self.Hands.append(card_value)
			#self.Cards_Amount -= 1
			#self.Cards[card_value] -= 1

			if (len(self.Hands) > 2):
				self.pre_operations.append("Hit")

			return(True)
		else:
			return(False)

	def dealer_push(self, card_value):
		if (self.Cards[card_value] > 0):
			#self.Cards_Amount -= 1
			#self.Cards[card_value] -= 1
			self.Dealer.append(card_value)

			return(True)
		else:
			return(False)

	def card_pass(self, card_value):
		if (self.Cards[card_value] > 0):
			self.Cards_Amount -= 1
			self.Cards[card_value] -= 1
			return(True)
		else:
			return(False)

if (__name__ == '__main__'):

	print("start searching at: ", datetime.datetime.now())

	test = BJ_analyzer(1)
	test.clear()

	test.hand_push(1)
	test.card_pass(1)
	test.hand_push(1)
	test.card_pass(1)
	test.hand_push(9)
	test.card_pass(9)

	test.dealer_push(1)
	test.card_pass(1)

	print("hand cards:\t", test.Hands)
	print("dealer cards:\t", test.Dealer)

	Eq = test.iter_hands(test.Hands)

	print("\nStrategies:")
	for key in Eq:
		print(key, ": ", Eq[key])

	print("end searching at: ", datetime.datetime.now())


	pro_bet = {}
	pro_bet["<13"] = 0
	pro_bet["=13"] = 0
	pro_bet[">13"] = 0

	work = BJ_analyzer(1)
	work.clear()

	for aa1 in range(10):
		a1 = aa1 + 1

		ratio1 = work.Cards[a1] / work.Cards_Amount
		work.dealer_push(a1)
		work.card_pass(a1)

		for aa2 in range(10):
			a2 = aa2 + 1

			ratio2 = work.Cards[a2] / work.Cards_Amount
			work.hand_push(a2)
			work.card_pass(a2)

			for aa3 in range(aa2, 10):
				a3 = aa3 + 1

				ratio3 = work.Cards[a3] / work.Cards_Amount
				if (aa3 != aa2):
					ratio3 *= 2
				work.hand_push(a3)
				work.card_pass(a3)

				ratio = ratio3 * ratio2 * ratio1
				print(a1,"\t", a2,"\t", a3, "\tratio: ", ratio)

				if (a2 + a3 < 13):
					pro_bet["<13"] += ratio
				if (a2 + a3 == 13):
					pro_bet["=13"] += ratio
				if (a2 + a3 > 13):
					pro_bet[">13"] += ratio

				work.clear()
				work.dealer_push(a1)
				work.card_pass(a1)
				work.hand_push(a2)
				work.card_pass(a2)

			work.clear()
			work.dealer_push(a1)
			work.card_pass(a1)

		work.clear()

	print("pro < 13: ", pro_bet["<13"], "\tpro = 13: ", pro_bet["=13"], "\tpro > 13: ", pro_bet[">13"])


	"""
	work = BJ_analyzer(0.75)
	work.clear()

	total_profit = 0
	for aa1 in range(10):
		a1 = aa1 + 1
		ratio1 = work.Cards[a1] / work.Cards_Amount
		work.dealer_push(a1)
		work.card_pass(a1)

		for aa2 in range(10):
			a2 = aa2 + 1
			ratio2 = work.Cards[a2] / work.Cards_Amount
			work.hand_push(a2)
			work.card_pass(a2)

			for aa3 in range(aa2, 10):
				a3 = aa3 + 1
				ratio3 = work.Cards[a3] / work.Cards_Amount
				if (aa3 != aa2):
					ratio3 *= 2
				work.hand_push(a3)
				work.card_pass(a3)

				ratio = ratio1 * ratio2 * ratio3
				print("dealer: ", work.Dealer,  "\thands: ", work.Hands,  "\tratio: ", ratio)

				eq_dict = work.iter_hands(work.Hands)

				opt_profit = -10
				opt_strategy = "hehe"
				for key in eq_dict:
					if ( (key == "Buy_Insurance") or (key == "No_Insurance") ):
						tmp = eq_dict[key][0]
						if (tmp > opt_profit):
							opt_strategy = key
							opt_profit = tmp
					else:
						if (eq_dict[key] > opt_profit):
							opt_strategy = key
							opt_profit = eq_dict[key]

				if ( (a2 == 1) and (a3 == 10) ):
					opt_profit *= 1.5

				print("opt strategy: ", opt_strategy, "\tprofit: ", opt_profit)
				total_profit += opt_profit * ratio
				print("total_profit: ", total_profit)

				work.clear()
				work.dealer_push(a1)
				work.card_pass(a1)
				work.hand_push(a2)
				work.card_pass(a2)

			work.clear()
			work.dealer_push(a1)
			work.card_pass(a1)

		work.clear()
	"""
