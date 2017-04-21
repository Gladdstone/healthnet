import os


def make_choice_list(filepath):
    """
    Makes a list of tuples from the values presented in the filepath
    :param filepath: file that has the list of values
    :return:
    """
    list = []
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    print (fileDir)
    filename = os.path.join(fileDir, filepath)
    with open(filename) as file:
        for line in file:
            text = line.rstrip()
            value = line.lower().replace(' ', '_').rstrip()
            list.append((value, text))
    return list
#make_choice_list('data/test_types.txt')