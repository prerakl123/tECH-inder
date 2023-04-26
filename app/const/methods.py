import random
from app.const.constants import PRINTABLE_CHARS, UID, ID_FILE_PATH


def unique(ID) -> bool:
    with open(ID_FILE_PATH, 'r') as id_file:
        id_list = list(map(lambda x: x.lstrip().rstrip(), id_file.readlines()))
        id_file.close()

        if id_list.count(ID) == 0:
            id_file.close()
            return True
    return False


def append_id_to_file(ID):
    with open(ID_FILE_PATH, 'r') as id_file:
        id_list = list(map(lambda x: x.lstrip().rstrip(), id_file.readlines()))
        id_list.append(ID)
        id_file.close()

    with open(ID_FILE_PATH, 'w') as id_file:
        id_file.write('\n'.join(id_list))
        id_file.close()


def generate_id(id_type=UID, sample=False, append=False) -> str:
    if sample:
        return id_type + ''.join(random.choices(PRINTABLE_CHARS, k=32))
    _id = ''.join(random.choices(PRINTABLE_CHARS, k=32))
    while unique(_id) is False:
        _id = ''.join(random.choices(PRINTABLE_CHARS, k=32))
    if append:
        append_id_to_file(_id)
    return id_type + _id


if __name__ == '__main__':
    print(generate_id(UID))
    print(generate_id(sample=True))
