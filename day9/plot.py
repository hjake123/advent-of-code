# def plot(lrange, rrange):
#     '''
#     Plot the relative positions of head and tail.
#     '''
#     for y in reversed(range(lrange, rrange)):
#         for x in range(lrange, rrange):
#             printed = False
#             if x == head.x and y == head.y:
#                 print('H', end='')
#                 printed = True
#                 continue
#             for i in range(0, 9):
#                 if x == tails[i].x and y == tails[i].y:
#                     print(i+1, end='')
#                     printed = True
#                     break
#             if not printed and x == 0 and y == 0:
#                 print('s', end='')
#             elif not printed:
#                 print('.', end='')
#         print('')
#     print('')