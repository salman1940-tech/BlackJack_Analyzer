from analyzer import BJ_analyzer

work = BJ_analyzer(1.0)
work.clear()

pro = 0

for aa1 in range(10):
	a1 = aa1 + 1
	ratio1 = work.Cards[a1] / work.Cards_Amount
	work.hand_push(a1)

	for aa2 in range(10):
		a2 = aa2 + 1
		ratio2 = work.Cards[a2] / work.Cards_Amount

		work.hand_push(a2)

		pro += ratio1 * ratio2

		work.clear()
		work.hand_push(a1)

	work.clear()

	print(pro)
