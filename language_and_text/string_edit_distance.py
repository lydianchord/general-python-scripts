import sys
# import string

# VOWELS = set('aeiou')
# CONSONANTS = set(string.ascii_lowercase).difference(VOWELS)
DEFAULT_COST = 1.0      # 2.0


def alignment_cost(l1, l2):
    """
    Given a pair of letters, return the alignment cost based on whether the
    letters are identical, both vowels, both consonants, or a consonant and a
    vowel.
    """
    if l1 == l2:
        cost = 0.0
    # elif l1 in VOWELS and l2 in VOWELS:
        # cost = 0.5
    # elif l1 in CONSONANTS and l2 in CONSONANTS:
        # cost = 0.6
    # else:
        # cost = 1.2
    else:
        cost = 1.0
    return cost


def compare(target, source):
    """
    Given a target and source word with a start-of-word character, return a
    two-dimensional list containing the minimum edit distances for all of the
    substring comparisons starting from the start-of-word character.
    """
    n = len(target)
    m = len(source)
    distances = [[]] * m
    distances[0] = [float(x) for x in range(0, 2 * n, 2)]
    for i in range(1, m):
        distances[i] = [2.0 * i] + [0] * (n - 1)
    for j in range(1, n):
        for i in range(1, m):
            a_cost = alignment_cost(source[i], target[j])
            # round to eliminate floating point imprecision in output
            distances[i][j] = round(min(distances[i-1][j] + DEFAULT_COST,
                                        distances[i-1][j-1] + a_cost,
                                        distances[i][j-1] + DEFAULT_COST), 1)
    return distances


def best_path(distances, target, source):
    """
    Given a two-dimensional list of minimum edit distances, a target word, and
    a source word, find the best path and print a grid containing all of the
    insertions, deletions, and alignments on the path. Then print a grid
    containing the minimum edit distance at each point on the path.
    """
    n = len(target)
    m = len(source)
    i, j = m - 1, n - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        current_cell = distances[i][j]
        if round(distances[i-1][j] + DEFAULT_COST, 1) == current_cell:
            coord = (i - 1, j)
        elif round(distances[i][j-1] + DEFAULT_COST, 1) == current_cell:
            coord = (i, j - 1)
        else:
            coord = (i - 1, j - 1)
        path.append(coord)
        i, j = coord
    path.reverse()
    
    header = '\n  ' + ''.join('%-5s' % x for x in target)
    path_grid = [[''] * n for i in range(m)]
    
    prev_i, prev_j = None, None
    for i, j in path:
        if i == prev_i:
            match = '*:' + target[j]
        elif j == prev_j:
            match = source[i] + ':*'
        else:
            match = source[i] + ':' + target[j]
        path_grid[i][j] = match
        prev_i, prev_j = i, j
    print(header)
    for i in range(len(path_grid)):
        line = source[i] + ' ' + ''.join('%-5s' % x for x in path_grid[i])
        print(line)
    
    print('\n' + '-' * len(line))
    for i, j in path:
        path_grid[i][j] = distances[i][j]
    print(header)
    for i in range(len(path_grid)):
        print(source[i] + ' ' + ''.join('%-5s' % x for x in path_grid[i]))


if __name__ == '__main__':
    try:
        target = '@' + sys.argv[1].lower()
        source = '@' + sys.argv[2].lower()
        verbose = True if len(sys.argv) > 3 and sys.argv[3] == '-v' else False
    except IndexError:
        sys.exit('\nSample usage: python string_edit_distance.py lead led')
    distances = compare(target, source)
    if verbose:
        for row in distances:
            print(''.join('%-5s' % x for x in row))
        print('')
    best_path(distances, target, source)
