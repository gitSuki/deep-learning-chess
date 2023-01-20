import random

def find_random_move(legal_moves):
    # randint is inclusive of last value
    random_index = random.randint(0, len(legal_moves) - 1)
    return legal_moves[random_index]
