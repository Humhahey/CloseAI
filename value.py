class Value:
    stack = []

    def __init__(self, data, label=""):
        self.grad = 1
        self.data = data
        self.label = label

    def __add__(self, other):
        out = Value(self.data + other.data)

        def _backward():
            self.grad *= out.grad
            other.grad *= out.grad

        out._backward = _backward
        self.stack.append(out)
        return out

    def __mul__(self, other):
        out = Value(self.data * other.data)

        def _backward():
            self.grad *= out.grad * other.data
            other.grad *= out.grad * self.data

        out._backward = _backward
        self.stack.append(out)
        return out

    def __repr__(self):
        return f"label:{self.label}|data:{self.data}|grad:{self.grad}"

    def result(self):
        if not self.stack:
            self.stack.pop._backward()
