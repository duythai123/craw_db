NUM_OF_LINES = 20000
filename = './virusDB/output'
for i in range(848):
    with open(filename+'{}.txt'.format(i), "rb") as fin:
        fout = open("output{}0.txt".format(i), "wb")
        for j, line in enumerate(fin):
            print(line)
            fout.write(line)
            if (j + 1) % NUM_OF_LINES == 0:
                print('Print file output{}'.format(j))
                fout.close()
                fout = open("output{}%d.txt".format(i) % (j / NUM_OF_LINES + 1), "wb")

        fout.close()
