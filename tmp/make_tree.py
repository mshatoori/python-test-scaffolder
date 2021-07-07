import libcst as cst

if __name__ == '__main__':
    with open('test_test.py', 'r') as in_file, open('tree', 'w') as out_file:
        tree = cst.parse_module(in_file.read())
        out_file.write(str(tree))
