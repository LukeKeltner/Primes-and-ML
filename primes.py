import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

total_numbers_considered = []
total_scores = []
even_scores = []
odd_scores = []
fifty_percent_scores = []

def run(total_number):
	total_numbers_considered.append(total_number)
	number = []
	digits = []
	primes = []
	max_number = total_number
	max_length = len(str(max_number))

	def getPrimes(N):
		primes_to_check = []
		primes_to_return = []

		for n in range(2, N+1):

			prime = True

			for i in primes_to_check:

				if n%i==0:

					prime = False

			if(prime):
				primes_to_return.append(1)
			else:
				primes_to_return.append(0)

			if (n**2 < N and prime):
				primes_to_check.append(n)

		return primes_to_return


	primes = getPrimes(max_number)

	for i in range(2, max_number+1):

		numbers = []
		for d in str(i):
			numbers.append(int(d))

		if len(str(i)) < max_length:
			for neg_one in range(max_length-len(str(i))):
				numbers.insert(0,-1)
		digits.append(numbers)
		number.append(i)

	new_digits = []

	for digit in range(len(digits[0])):
		new_digit_column = []
		for num in range(len(number)):
			new_digit_column.append(digits[num][digit])
		new_digits.append(new_digit_column)

	dictionary = {"Number": number, "Prime": primes}
	for digit_column in range(len(new_digits)):
		dictionary[str(10**(len(new_digits)-digit_column-1))] = new_digits[digit_column]

	primes_df = pd.DataFrame(dictionary)
	features = primes_df.drop("Prime", axis=1).columns.values
	primes_df = shuffle(primes_df)

	train = primes_df[0: round(max_number*.8)]
	test = primes_df[round(max_number*.8)+1: max_number]
	test_evens = test[test["Number"]%2==0]
	test_odds = test[test["Number"]%2==1]

	features = primes_df.drop("Prime", axis=1).columns.values
	clf = RandomForestClassifier(max_depth=2, random_state=0)
	clf.fit(train[features], train["Prime"])

	total_score = clf.score(test[features], test["Prime"])
	total_scores.append(total_score)

	even_score = clf.score(test_evens[features], test_evens["Prime"])
	even_scores.append(even_score)

	odd_score = clf.score(test_odds[features], test_odds["Prime"])
	odd_scores.append(odd_score)

max_run = 9999
min_run = 50

for i in range(min_run, max_run):
	print(str(round((i-min_run)/(max_run-min_run)*100,2))+"% complete. Finished with number "+str(i-1))
	run(i)

def fit_func(x, a, b, c):
	return a * np.log(b * x) + c

total_numbers_considered = np.array(total_numbers_considered)
total_scores = np.array(total_scores)
even_scores = np.array(even_scores)
odd_scores = np.array(odd_scores)

popt_total, pcov_total = curve_fit(fit_func, total_numbers_considered, total_scores)
popt_even, pcov_even = curve_fit(fit_func, total_numbers_considered, even_scores)
popt_odd, pcov_odd = curve_fit(fit_func, total_numbers_considered, odd_scores)

plt.plot(total_numbers_considered, total_scores, label="Total Score")
plt.plot(total_numbers_considered, even_scores, label="Evens Score")
plt.plot(total_numbers_considered, odd_scores, label="Odds Score")
plt.plot(total_numbers_considered, fit_func(total_numbers_considered, *popt_total), 'b-', label='Total fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_total))
plt.plot(total_numbers_considered, fit_func(total_numbers_considered, *popt_even), 'r-', label='Even fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_even))
plt.plot(total_numbers_considered, fit_func(total_numbers_considered, *popt_odd), 'g-', label='Odd fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt_odd))

plt.legend(loc=4)
plt.show()
