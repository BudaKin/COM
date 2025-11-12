import komm


code = komm.BlockCode([[1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 0],])

# code.length = 6 (n)
# code.dimension = 3 (k)
# code.codewords() array([[0, 0, 0, 0, 0, 0],
#                         [1, 0, 0, 0, 1, 1],
#                         [0, 1, 0, 1, 0, 1],
#                         [1, 1, 0, 1, 1, 0],
#                         [0, 0, 1, 1, 1, 0],
#                         [1, 0, 1, 1, 0, 1],
#                         [0, 1, 1, 0, 1, 1],
#                         [1, 1, 1, 0, 0, 0]])

import math
rep31 = komm.RepetitionCode(3) # codigo (3,1)
# rep31.length = 3 (n)
# rep31.dimension = 1 (k)
# rep31.generator_matrix = array([[1, 1, 1]])
# rep31.encode(0, 0, 1, 1, 0) = retorna o código com cada bit de parametro transformado para b

spc32 = komm.SingleParityCheckCode(3)
# rep31.length = 3 (n)
# rep31.dimension = 2 (k)
# spc32.generator_matrix = array([[1, 0, 1],
#                                 [0, 1, 1]])

hamming74 = komm.HammingCode(3) # p1, p2, p3, portanto parametro 3 (mu)
# hamming74.length, hamming74.dimension = (7, 4)
# hamming74.chech_matrix = H
# hamming74.generator_matrix = G
# H.T = H transposto
