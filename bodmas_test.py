import sys

class Calculator:
	def __init__(self, expr) -> None:
		
		# output presentation variables
		self.input = expr
		self.steps = []
		self.output = None

		self.expr = expr


	def validate(self) -> bool:
		# validate expression string

		if len(self.expr) == 0:
			return False

		self.expr = self.expr.replace(" ", "")
		self.expr = list(self.expr)

		# if the expression starts with a decimal point, closing parentheses,
		# multiplication and division sign
		if self.expr[0] in [".", ")", "*", "/"]:
			return False

		for i, char in enumerate(self.expr):
			# if a char is not numeric, opertion sign or decimal point
			if char not in '0123456789+-*/.()|':
				return False

			# if there is no operation sign between a number and parentheses
			if char.isnumeric() and i+1 < len(self.expr) and self.expr[i + 1] == "(":
				return False

		return True

	def solve(self, num_list, op_list):
		for x,y in enumerate(op_list):
			if y == '**':
				# if an exponential operator is detected

				# appending operation to steps
				self.steps.append('\nRaising power {} to {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) ** num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				del num_list[x+1]
				op_list.remove(y)
				
		for x,y in enumerate(op_list):
			if y == '/':
				# if an division operator is detected

				# appending operation to steps
				self.steps.append('\nDividing {} by {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) / num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				del num_list[x+1]
				op_list.remove(y)

			if y == '*':
				# if an multiplication operator is detected

				# appending operation to steps
				self.steps.append('\nMultiplying {} and {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) * num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				del num_list[x+1]
				op_list.remove(y)

		for x,y in enumerate(op_list):
			if y == '+':
				# if an addition operator is detected

				# appending operation to steps
				self.steps.append('\nAdding {} and {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) + num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				del num_list[x+1]
				op_list.remove(y)

			if y == '-':
				# if an subtraction operator is detected

				# appending operation to steps
				self.steps.append("Subtracting {} from {}".format(num_list[x+1], num_list[x]))

				num_list[x] = float(num_list[x]) - num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				del num_list[x+1]
				op_list.remove(y)

		return num_list, op_list

	def solve_equation(self, equation) -> float:

		temp = ''
		num_list = []
		op_list = []
		openparentheses_count = 0
		absolute_operator_count = 0

		count = 0
		while count < len(equation):

			# if opening parentheses is encountered 
			# seperate out the substring between the parentheses
			# solve the parentheses
			if str(equation[count]) == "(":
				openparentheses_count += 1
				if openparentheses_count > 1:
					temp += equation[count]
				count += 1
				continue
			elif str(equation[count]) == ")":
				openparentheses_count -= 1
				if openparentheses_count == 0:
					temp = self.solve_equation(temp)
					num_list.append(float(temp))
					temp = ''
				else:
					temp += equation[count]
				count += 1
				continue
			
			# if an absolute operator is detected
			if str(equation[count]) == '|' and openparentheses_count == 0:
				if absolute_operator_count == 1:
					absolute_operator_count = 0
					temp = abs(float(eval(temp)))
					num_list.append(temp)
					temp = ''
				else:
					absolute_operator_count += 1
				count += 1
				continue

			
			# if at any point closing parentheses are before opening parentheses
			if openparentheses_count < 0:
				sys.stderr.write("Invalid Expression\n")
				sys.exit()
			
			if openparentheses_count > 0 or absolute_operator_count > 0:
				# if parentheses are open
				temp += str(equation[count])
				count += 1
			else:
				
				if equation[count] in '1234567890.':
					# if the equation[count]acter is a numeric
					try:
						if equation[count-1] in '-+':
							if count == 1 or equation[count-2] in '-+*/)':
								op_list.pop()
								temp+=equation[count-1]
					except Exception as e:
						pass
					temp = temp + str(equation[count]) 
				else:
					# if a number is found
					if temp != '':
						num_list.append(float(temp))
					temp = ''

					# operator list
					if equation[count] == "*" and equation[count+1] == "*": 
						op_list.append("**")
						del equation[count+1]
					else:
						op_list.append(equation[count])

				# if the list has been traversed completely	
				if count+1 is len(equation):
					num_list.append(float(temp))
					temp = ''
				count += 1

		# solving the equation and appendin the steps
		num_list, op_list = self.solve(num_list, op_list)
		while ('+' in op_list) or ('-' in op_list) or ('*' in op_list) or ('/' in op_list) or ('^' in op_list):
			num_list, op_list = self.solve(num_list, op_list)

		return num_list[0]


	def calculate(self) -> float:

		# if an invalid string is detected
		if not self.validate():
			sys.stderr.write("Invalid Expression\n")
			sys.exit()

		try:
			self.output = self.solve_equation(self.expr)
		except Exception as e:
			sys.stderr.write("Invalid Expression\n")
			sys.exit()

		# printing the output
		self.present_output()

	def present_output(self):

		# presents the output
		print('\nINPUT: {}'.format(self.input))
		print('OUTPUT: {}'.format(self.output))

		print("\nSTEP BY STEP CALCULATION")

		for step in self.steps:
			print(step)

if __name__ == "__main__":
	# expr = input("Enter the expression:\n")
	with open('example.txt') as f:
		inputs = f.read().splitlines()
		for i, expr in enumerate(inputs):
			print("############ {}".format(str(i)))
			calculator = Calculator(expr)
			calculator.calculate()
		f.close()