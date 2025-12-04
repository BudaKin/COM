import komm
import string

lz77 = komm.LempelZiv77Code(
    window_size = 12, 
    lookahead_size = 4, 
    source_cardinality = 27
    )

calX = " " + string.ascii_lowercase

msg = [calX.index(x) for x in "a asa da casan"]
print(msg)
tokens = lz77.source_to_tokens(msg)
print(tokens)
compressed = lz77.tokens_to_target(tokens)
print(compressed)