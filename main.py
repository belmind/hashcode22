from os import walk

import solve


# Hardcoded output file names
output_files = [
  'out/a_out',
  'out/b_out',
  'out/c_out',
  'out/d_out',
  'out/e_out',
  'out/f_out',
]


def build_paths():
    """ Reads files from './in' directory and maps to appropriate output
    file name.
    """
    _, _, input_files = next(walk('./in'))
    _input_files = sorted(input_files)
    input_files = ['in/' + input_file for input_file in _input_files]
    return sorted(set(zip(input_files, output_files)), key=lambda t: t[1])


def main(file):
    """ The file handler. Reads all input files and passes the string to
    the solver. Write the solvers output string to the appropriate file.
    """
    with open(file[0], 'r') as inp, open(file[1], 'w') as out:
        # Call appropriate solver
        out_str = solve.solve(inp)
        # Create output file
        out.write(out_str)

        print(f'DONE: {file[0]}')


if __name__ == '__main__':
    files = build_paths()
    main(files[1])
    # for file in files:
    #     main(file)
