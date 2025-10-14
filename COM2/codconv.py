import komm
import numpy as np

# komm.ConvolutionalCode([[0b11, 0b10, 0b11],[0b10, 0b01, 0b01]])

code = komm.ConvolutionalCode([[0b111, 0b101]])

u = np.array([1,0,1,1,0,0,0])

v = code.encode(u)

print(u)
print(v)