
# Solver that takes an input as a file object,
# and returns the output as a string

def solve(input):
    final_ingredients = set()
    global_dislikes = set()

    nr_clients = int(input.readline())
    for _ in range(nr_clients):
        likes = input.readline().split()[1:]
        dislikes = input.readline().split()[1:]
        global_dislikes.update(dislikes)
        if any([dislike in final_ingredients for dislike in dislikes]):
            continue
        final_ingredients.update(likes)

    return str(len(final_ingredients)) + " " + " ".join(final_ingredients)
