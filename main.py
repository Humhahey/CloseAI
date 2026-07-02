from value import Value

x = Value(1, "x")
a = Value(2, "a")
b = Value(3, "b")

y = b + a * x
y.label = "y"
y.result()

print(a)
print(b)
print(x)
print(y)
