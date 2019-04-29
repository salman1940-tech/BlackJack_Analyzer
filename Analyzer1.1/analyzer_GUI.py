import analyzer
import tkinter as tk

class APP_tool:

	calculaters = []
	eq_dicts = []
	heap_ptr = 0

	decks = 1.0

	cards_passed = []
	dealer_cards = []

	Cards_dict = {}

	def __init__(self, master):

		new_calculater = analyzer.BJ_analyzer(self.decks)
		new_calculater.clear()
		self.calculaters.append(new_calculater)
		self.heap_ptr = 0
		self.eq_dicts.append(0)
	
		for ii in range(9):
			i = ii + 1
			self.Cards_dict[i] = int(self.decks * 4)
		self.Cards_dict[10] = 4 * int(self.decks * 4)

		frame = tk.Frame(master, height = 800, width = 1000)
		frame.pack()

		toolname = tk.Label(master, text = "BlackJack Analyzer By YU_Yeqing", font = 0.8)
		toolname.place(relx = 0.50,rely = 0.05, relheight = 0.05, relwidth = 0.4, anchor = tk.CENTER)

		decksLB = tk.Label(master, text = "Decks of Cards: ")
		decksLB.place(relx = 0.15, rely = 0.1, relheight = 0.05, relwidth = 0.2, anchor = tk.CENTER)
		self.decks_str = tk.StringVar(master)
		self.decks_str.set('1')
		self.decksBT = tk.OptionMenu(master, self.decks_str, '0.75', '1', '2', '3', '4', '5', '6')
		self.decksBT.place(relx = 0.15,rely = 0.15, relheight = 0.04, relwidth = 0.12, anchor = tk.CENTER)

		DealerCardLB = tk.Label(master, text = "Up Card of Dealer: ")
		DealerCardLB.place(relx = 0.15,rely = 0.25, relheight = 0.05, relwidth = 0.2, anchor = tk.CENTER)
		self.DealerCard_str = tk.StringVar(master)
		self.DealerCard_str.set("unknown")
		self.DealerCard_BT = tk.OptionMenu(master, self.DealerCard_str,'unknown', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10')
		self.DealerCard_BT.place(relx = 0.15,rely = 0.3, relheight = 0.04, relwidth = 0.12, anchor = tk.CENTER)

		self.push_dealer_button = tk.Button(frame, text = 'push', fg = 'blue', command = self.push_dealer)
		self.push_dealer_button.place(relx = 0.25,rely = 0.3, relheight = 0.04, relwidth = 0.07, anchor = tk.CENTER)

		HandCardLB = tk.Label(master, text = "Push Cards to Hands: ")
		HandCardLB.place(relx = 0.15,rely = 0.45, relheight = 0.05, relwidth = 0.2, anchor = tk.CENTER)
		self.HandCard_str = tk.StringVar(master)
		self.HandCard_str.set("unknown")
		self.HandCard_BT = tk.OptionMenu(master, self.HandCard_str, 'unknown', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10')
		self.HandCard_BT.place(relx = 0.15,rely = 0.5, relheight = 0.04, relwidth = 0.12, anchor = tk.CENTER)

		self.push_hands_button = tk.Button(frame, text = 'push', fg = 'blue', command = self.push_hands)
		self.push_hands_button.place(relx = 0.25,rely = 0.5, relheight = 0.04, relwidth = 0.07, anchor = tk.CENTER)

		PassCardLB = tk.Label(master, text = "Cards Passed: ")
		PassCardLB.place(relx = 0.15,rely = 0.65, relheight = 0.04, relwidth = 0.12, anchor = tk.CENTER)
		self.PassCard_str = tk.StringVar(master)
		self.PassCard_str.set("unknown")
		self.PassCard_BT = tk.OptionMenu(master, self.PassCard_str, 'unknown', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10')
		self.PassCard_BT.place(relx = 0.15,rely = 0.7, relheight = 0.04, relwidth = 0.12, anchor = tk.CENTER)

		self.push_passed_button = tk.Button(frame, text = 'push', fg = 'blue', command = self.push_passed)
		self.push_passed_button.place(relx = 0.25,rely = 0.7, relheight = 0.04, relwidth = 0.07, anchor = tk.CENTER)

		self.reset_button = tk.Button(frame, text = 'Reset', fg = 'blue', command = self.reset)
		self.reset_button.place(relx = 0.6,rely = 0.2, relheight = 0.04, relwidth = 0.1, anchor = tk.CENTER)

		self.calculate_button = tk.Button(frame, text = 'Calculate', fg = 'blue', command = self.calculate)
		self.calculate_button.place(relx = 0.8,rely = 0.2, relheight = 0.04, relwidth = 0.1, anchor = tk.CENTER)

		self.split_button = tk.Button(frame, text = 'Split', fg = 'blue', command = self.split)
		self.split_button.place(relx = 0.5, rely = 0.51, relheight = 0.04, relwidth = 0.08, anchor= tk.CENTER)

		self.up_heap_button = tk.Button(frame, text = 'Up', fg = 'blue', command = self.up_heap)
		self.up_heap_button.place(relx = 0.5, rely = 0.57, relheight = 0.04, relwidth = 0.05, anchor= tk.CENTER)

		self.down_heap_button = tk.Button(frame, text = 'Dn', fg = 'blue', command = self.down_heap)
		self.down_heap_button.place(relx = 0.5, rely = 0.61, relheight = 0.04, relwidth = 0.05, anchor= tk.CENTER)

		self.dateboard = tk.Text(master)
		self.dateboard.place(relx = 0.75,rely = 0.6, relheight = 0.7, relwidth = 0.4, anchor = tk.CENTER)

	def reset(self):

		self.decks = float(self.decks_str.get())

		self.calculaters.clear()

		new_calculater = analyzer.BJ_analyzer(self.decks)
		new_calculater.clear()

		self.calculaters.append(new_calculater)
		self.heap_ptr = 0

		self.eq_dicts.clear()
		self.eq_dicts.append(0)

		self.cards_passed.clear()

		self.dealer_cards.clear()

		self.Cards_dict = {}
		for ii in range(9):
			i = ii + 1
			self.Cards_dict[i] = int(self.decks * 4)
		self.Cards_dict[10] = 4 * int(self.decks * 4)

		self.dateboard_show()

	def calculate(self):

		if ( (len(self.calculaters[self.heap_ptr].Hands) >= 2) and (len(self.calculaters[self.heap_ptr].Dealer) >= 1) ):
			#self.dateboard_show(waiting = True)

			eq_dict = self.calculaters[self.heap_ptr].iter_hands(self.calculaters[self.heap_ptr].Hands.copy())
			self.eq_dicts[self.heap_ptr] = eq_dict

			self.dateboard_show(waiting = False)


	def push_dealer(self):

		if (self.DealerCard_str.get() == 'unknown'):
			P_dat = -1
		elif (self.DealerCard_str.get() == 'A'):
			P_dat = 1
		else:
			P_dat = int(self.DealerCard_str.get())

		if (P_dat != -1):
			if (self.Cards_dict[P_dat] > 0):
				self.dealer_cards.append(P_dat)
				self.cards_passed.append(P_dat)

				self.Cards_dict[P_dat] -= 1

				for ana in self.calculaters:
					ana.dealer_push(P_dat)
					ana.card_pass(P_dat)

		self.dateboard_show()

	def push_hands(self):

		if (self.HandCard_str.get() == 'unknown'):
			P_dat = -1
		elif (self.HandCard_str.get() == 'A'):
			P_dat = 1
		else:
			P_dat = int(self.HandCard_str.get())

		if (P_dat != -1):
			if (self.Cards_dict[P_dat] > 0):

				self.cards_passed.append(P_dat)
				self.Cards_dict[P_dat] -= 1

				self.calculaters[self.heap_ptr].hand_push(P_dat)

				for ana in self.calculaters:
					ana.card_pass(P_dat)

				for i in range(len(self.eq_dicts)):
					self.eq_dicts[i] = 0

		self.dateboard_show()

	def push_passed(self):

		if (self.PassCard_str.get() == 'unknown'):
			P_dat = -1
		elif (self.PassCard_str.get() == 'A'):
			P_dat = 1
		else:
			P_dat = int(self.PassCard_str.get())

		if (P_dat != -1):
			if (self.Cards_dict[P_dat] > 0):

				self.cards_passed.append(P_dat)
				self.Cards_dict[P_dat] -= 1

				for ana in self.calculaters:
					ana.card_pass(P_dat)

				for i in range(len(self.eq_dicts)):
					self.eq_dicts[i] = 0

		self.dateboard_show()

	def split(self):

		if ( (len(self.calculaters[self.heap_ptr].Hands) == 2) and (self.calculaters[self.heap_ptr].Hands[0] == self.calculaters[self.heap_ptr].Hands[1])):
			self.calculaters[self.heap_ptr].pre_operations.append("Split")

			new_calculater = analyzer.BJ_analyzer(self.decks)
			new_calculater.clear()
			new_calculater.pre_operations = self.calculaters[self.heap_ptr].pre_operations.copy()
			new_calculater.hand_push(self.calculaters[self.heap_ptr].Hands[0])
			self.calculaters[self.heap_ptr].Hands = self.calculaters[self.heap_ptr].Hands[:-1]

			for p in self.dealer_cards:
				new_calculater.dealer_push(p)

			for p in self.cards_passed:
				new_calculater.card_pass(p)

			self.eq_dicts[self.heap_ptr] = 0
			self.eq_dicts.append(0)
			self.calculaters.append(new_calculater)

		self.dateboard_show()

	def up_heap(self):
		if (self.heap_ptr > 0):
			self.heap_ptr -= 1
			self.dateboard_show()

	def down_heap(self):
		if (self.heap_ptr < len(self.calculaters) - 1):
			self.heap_ptr += 1
			self.dateboard_show()

	def dateboard_show(self, waiting = False):

		output_text = "Remaining Cards: \n\n"

		for key in self.Cards_dict:
			if (key == 1):
				output_text += 'A\t' + str(self.Cards_dict[key]) + '\n'
			else:
				output_text += str(key) + '\t' + str(self.Cards_dict[key]) + '\n'

		output_text += '\n---------------------------------------------------\n'

		output_text += "\nDealer Cards: "
		for p in self.dealer_cards:
			if (p == 1):
				output_text += 'A '
			else:
				output_text += str(p) + ' '
		output_text += "\n\n---------------------------------------------------\n\n"

		n = -1
		for ana in self.calculaters:
			n += 1
			output_text += "Hand Cards: "
			for p in ana.Hands:
				if (p == 1):
					output_text += 'A '
				else:
					output_text += str(p) + ' '
			if (self.heap_ptr == n):
				output_text += '\t<-\n'
			else:
				output_text += '\n'

		output_text += '\n---------------------------------------------------\n\n'

		if (waiting):
			output_text += "Calculating......\n"
		else:
			if (self.eq_dicts[self.heap_ptr] == 0):
				output_text += "No avaliable data\n"
			else:
				output_text += "Equityedge:\n\n"
				eq_dict = self.eq_dicts[self.heap_ptr]
				opt_profit1 = -10
				opt_strategy1 = "unknown"
				for key in eq_dict:
					if ( (key == "Buy_Insurance") or (key == "No_Insurance") ):
						tmp = eq_dict[key][0]
						if (tmp > opt_profit1):
							opt_strategy1 = key
							opt_profit1 = tmp

						output_text += key + ":\t" + str(tmp) + '\n'

						for key2 in eq_dict[key][1]:
							output_text += "\t" + key2 + ":\t" + str(eq_dict[key][1][key2]) + '\n'
					else:
						output_text += key + ":\t" + str(eq_dict[key]) + '\n'
						tmp = eq_dict[key]
						if (tmp > opt_profit1):
							opt_strategy1 = key
							opt_profit1 = tmp
				output_text += '\n'

				if ( (opt_strategy1 == "Buy_Insurance") or (opt_strategy1 == "No_Insurance") ):
					opt_profit2 = -10
					opt_strategy2 = 'unknown'
					for key2 in eq_dict[opt_strategy1][1]:
						tmp = eq_dict[opt_strategy1][1][key2]
						if (tmp > opt_profit2):
							opt_strategy2 = key2
							opt_profit2 = tmp

					output_text += "optimal strategy: " + opt_strategy1 + "->" + opt_strategy2 + '\n'
				else:
					output_text += "optimal strategy: " + opt_strategy1 + '\n'


		self.dateboard.delete(1.0,tk.END)
		self.dateboard.insert(tk.INSERT, output_text)
		pass

if (__name__ == "__main__"):

	root = tk.Tk()
	root.title("Analyzer GUI")
	root.resizable(width = False, height = False)
	app = APP_tool(root)

	root.mainloop()
