import utils

current_version = int(utils.get_maldb_ver())

with open("./virusDB/output{}0.txt".format(current_version + 1), "rb") as fin:
    for i, line in enumerate(fin):
        print(line)
        try:
            utils.get_virus_infos(line)
        except Exception as ex:
            print(ex)
            print('error line')

utils.update_version(current_version)
fin.close()
