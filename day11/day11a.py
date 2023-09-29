from collections import deque

class monkey:
    def __init__(self):
        self.items = deque()
        self.loperation = ''
        self.operation = ''
        self.roperation = ''
        self.test_modulo = 1 
        self.true_target = 0
        self.false_target = 0
        self.activity = 0

    def parse_argument(self, s, item):
        if s == 'old':
            a = item
        else:
            a = int(s)
        return a
            
    def take_turn(self):
        global monkeys
        counter = 0
        while counter < len(self.items):
            item = self.items.pop()
            # First, perform the operation.
            l = self.parse_argument(self.loperation, item)
            r = self.parse_argument(self.roperation, item)
            
            if self.operation == '+':
                item = l + r
            elif self.operation == '*':
                item = l * r

            # Divide by three.
            item = int(item / 3)

            # Increment activity.
            self.activity += 1

            # Check if the item worry is divisible by test_modulo, and send it accordingly.
            if(item % self.test_modulo == 0):
                monkeys[self.true_target].items.appendleft(item)
            else:
                monkeys[self.false_target].items.appendleft(item)

monkeys = []

with open('day11/in.txt') as file:
    m = None
    for line in file:
        words = line.split()
        if len(words) == 0:
            continue

        match words[0]:
            case 'Monkey':
                if not m == None:
                    monkeys.append(m)
                m = monkey()
            case 'Starting':
                m.items = deque(reversed([int(n) for n in [word.split(',')[0] for word in words[2:]]]))
            case 'Operation:':
                m.loperation = words[3]
                m.operation = words[4]
                m.roperation = words[5]
            case 'Test:':
                m.test_modulo = int(words[3])
            case 'If':
                if words[1] == 'true:':
                    m.true_target = int(words[5])
                elif words[1] == 'false:':
                    m.false_target = int(words[5])
    monkeys.append(m)

for _ in range(20):
    for m in monkeys:
        m.take_turn()

heighest_act = -1
second_heighest_act = -2

for monkey in monkeys:
    if monkey.activity > heighest_act:
        second_heighest_act = heighest_act
        heighest_act = monkey.activity
    elif monkey.activity > second_heighest_act:
        second_heighest_act = monkey.activity

print(heighest_act * second_heighest_act)