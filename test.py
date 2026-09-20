#
# num1 = 12
# num2 = 5
# soma = num1 + num2
# print(soma)
#
# def soma(num1: int, num2: int):
#     return num1+num2

class Calculadora:

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def soma(self):
        return self.num1 + self.num2

    def subtracao(self):
        return self.num1 - self.num2

    def mulltiplicacao(self):
        return self.num1 * self.num2

    def edmilson(self):
        return self.num1 / self.num2


cal = Calculadora(20, 2)



print(cal.mulltiplicacao())

