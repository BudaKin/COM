import komm

convcode = komm.ConvolutionalCode([0b111, 0b101])

blockcode = komm.TerminatedConvolutionalCode(convolutional_code=convcode,num_blocks=5,mode="direct-truncation") # Transformação conv -> block (Terminação truncamento direto)

nk = (blockcode.length, blockcode.dimension)

blockcode.generator_matrix

blockcode.minimum_distance()

blockcode.encode([1,0,1,1,0]) # 11 10 00 01 01

blockcode = komm.TerminatedConvolutionalCode(convolutional_code=convcode,num_blocks=5,mode="zero-termination") # Transformação conv -> block (Terminação estado 0)

nk = (blockcode.length, blockcode.dimension)

blockcode.generator_matrix

blockcode.minimum_distance()

blockcode.encode([1,0,1,1,0]) # 11 10 00 01 01 11 00

blockcode = komm.TerminatedConvolutionalCode(convolutional_code=convcode,num_blocks=5,mode="tail-biting") # Transformação conv -> block ("Mordida de cauda")
# Tail biting começa e termina no mesmo estado.
nk = (blockcode.length, blockcode.dimension)

blockcode.generator_matrix

blockcode.minimum_distance()

blockcode.encode([1,0,1,1,0]) # 00 10 00 01 01