
def main():
    troops = {}
    with open('ykkös_lippukunnat.txt', 'r', encoding='utf-8') as cleaned_file:
        for row in cleaned_file:
            row  = row.strip()
            try:
                troops[row] += 1
            except KeyError:
                troops[row] = 1
    with open("lippukunnat_jäsenmäärät.csv", "a") as myfile:
        for troop in troops.keys():
            if not troop.startswith("HP"):
                print(troops[troop])
                print(repr(troop))
                line = ";{0};{1};\n".format(repr(troop), troops[troop])
                print(line)
                myfile.write(line)



if __name__ == "__main__":

    main()