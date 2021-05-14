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

		self.expr = self.expr.replace(" ", "")
		self.expr = list(self.expr)

		# if the expression starts with a decimal point, closing parentheses,
		# multiplication and division sign
		if self.expr[0] in [".", ")", "*", "/"]:
			return False

		for i, char in enumerate(self.expr):
			# if a char is not numeric, opertion sign or decimal point
			if char not in '0123456789+-*/.()':
				return False

			# if there is no operation sign between a number and parentheses
			if char.isnumeric() and self.expr[i + 1] == "(":
				return False

		return True

	def solve(self, num_list, op_list):
		for x,y in enumerate(op_list):
			if y == '^':
				# if an exponential operator is detected

				# appending operation to steps
				self.steps.append('Raising power {} to {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) ** num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				num_list.remove(num_list[x+1])
				op_list.remove(y)
		for x,y in enumerate(op_list):
			if y == '/':
				# if an division operator is detected

				# appending operation to steps
				self.steps.append('Dividing {} by {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) / num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				num_list.remove(num_list[x+1])
				op_list.remove(y)
		for x,y in enumerate(op_list):
			if y == '*':
				# if an multiplication operator is detected

				# appending operation to steps
				self.steps.append('Multiplying {} and {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) * num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				num_list.remove(num_list[x+1])
				op_list.remove(y)
		for x,y in enumerate(op_list):
			if y == '+':
				# if an addition operator is detected

				# appending operation to steps
				self.steps.append('\nAdding {} and {}'.format(num_list[x], num_list[x+1]))

				num_list[x] = float(num_list[x]) + num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				num_list.remove(num_list[x+1])
				op_list.remove(y)
		for x,y in enumerate(op_list):
			if y == '-':
				# if an subtraction operator is detected

				# appending operation to steps
				self.steps.append("Subtracting {} from {}".format(num_list[x+1], num_list[x]))

				num_list[x] = float(num_list[x]) - num_list[x+1]

				# appending output of the operation to steps
				self.steps.append(num_list[x])

				num_list.remove(num_list[x+1])
				op_list.remove(y)
		return num_list, op_list

	def solve_equation(self, equation) -> float:

		temp = ''
		num_list = []
		op_list = []
		openparentheses_count = 0

		for i,char in enumerate(equation):

			# if opening parentheses is encountered 
			# seperate out the substring between the parentheses
			# solve the parentheses
			if str(char) == '(':
				openparentheses_count += 1
				if openparentheses_count > 1:
					temp += str(char)
				continue 
			elif str(char) == ')':
				openparentheses_count -= 1
				if openparentheses_count == 0:
					temp= self.solve_equation(temp)
					num_list.append(temp)
				else:
					temp += str(char)
				continue
			
			# if at any point closing parentheses are before opening parentheses
			if openparentheses_count < 0:
				sys.stderr.write("Invalid Expression")
			
			if openparentheses_count > 0:
				# if parentheses are open
				temp += str(char)
			else:
				
				if str(char) in '0123456789.':
					# if the character is a numeric
					temp = temp + str(char) 
				else:
					# if a number is found
					if temp != '':
						num_list.append(float(temp))
					temp = ''

					# operator list 
					op_list.append(char)

				# if the list has been traversed completely	
				if i+1 is len(equation):
					num_list.append(float(temp))
					temp = ''

		# solving the equation and appendin the steps
		num_list, op_list = self.solve(num_list, op_list)

		return num_list[0]

	def calculate(self) -> float:

		# if an invalid string is detected
		if not self.validate():
			sys.stderr.write("Invalid Expression")

		self.output = self.solve_equation(self.expr)

		# printing the output
		self.present_output()

	def present_output(self):

		# presents the output
		print('\nINPUT: {}'.format(self.input))
		print('OUTPUT: {}'.format(self.output))

		print("\nSTEP BY STEP CALCULATION\n")

		for step in self.steps:
			print(step)


if __name__ == "__main__":
	expr = input("Enter the expression:\n")
	calculator = Calculator(expr)
	calculator.calculate()