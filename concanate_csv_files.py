import glob

def main(years):
    for year in years:
        i = 0
        with open('cleaned_csv\\HP_liittyneet_vuosi_{0}_vuosi.csv'.format(str(year)), 'w') as outfile:
            for kuksa_file_csv in glob.glob('cleaned_csv\\*{0}_kuukausi.csv'.format(str(year))):
                with open(kuksa_file_csv) as infile:
                    for line in infile:
                        outfile.write(line)
                        i+=1
                infile.close
        outfile.close
        print(i)

if __name__ == "__main__":
    years = [2014, 2015]

    main(years)