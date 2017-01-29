# -*- coding: utf-8 -*-
#This script is used for removing columns that are not needed for one reason or other from
#Kuksa registery csv file

from __future__ import unicode_literals
import configparser
import xlrd
import os

first = True

def csv_from_excel(excel_file, excel_sheetname):
    wb = xlrd.open_workbook(excel_file)
    sh = wb.sheet_by_name(excel_sheetname)
    filename , file_extension = os.path.splitext(excel_file)
    csv_filename = filename+'.csv'

    with open(csv_filename, 'w') as csv_file:
        for rownum in range(sh.nrows):
            csv_row=';'
            for value in sh.row_values(rownum):
                #print(value)
                csv_row += str(value)+';'
            csv_row += '\n'
            csv_file.write(csv_row)

    csv_file.close()
    print
    return csv_filename.split('\\')

def get_excel_files_in_folder(folder):
    import glob
    return glob.glob(folder+'*.xlsx')

def create_config_file():
    config = configparser.RawConfigParser()
    config.add_section('general')
    config.set('general', 'comma_separated_columns', 'Sukunimi,Etunimi')
    config.set('general', 'kuksa_membership_register_filename', 'example.csv')
    
    with open('clean_columns.cfg', 'wb') as configfile:
        config.write(configfile)

def select_columns(first_line):
    columns = []
    print("Choosing columns which are to be cleaned")
    which_columns=True
    while which_columns:
        for field in first_line:
            #print(field)
            clean_input = input("From kuksa file Clean column:'{0}'?(y/n)".format( field))
            print(clean_input)
            if clean_input == 'y':
                columns.append(True)
            else:
                columns.append(False)
        print('Showing selection')
        i = 0
        for field in first_line:
            if columns[i]:
                print('Cleaning column {0}'.format(field))
            else:
                print('Keeping column {0}'.format(field))
            i+=1
        is_correct = input('Is this correct? (y/n)')
        if is_correct == 'y':
            which_columns = False
        else:
            print('Restarting selection')
            columns = []
    return columns

def read_and_clean_kuksa_file(columns, kuksa_filename):

    global first
    with open(kuksa_filename, 'r') as file:
        columns_to_be_cleaned = []
        for row in file:
            #print(first)
            fields = row.split(';')
            if first and len(columns) <= 1:
                columns_to_be_cleaned = select_columns(fields)
            elif first and len(columns) > 1:
             #   print(columns)
                for field in fields:
                    if field in columns:
              #          print(field)
                        columns_to_be_cleaned.append(False)
                    else:
                        columns_to_be_cleaned.append(True)
            first=False

            #print(columns_to_be_cleaned)
            #print(row)
            cleaned_row = ''
            i=0
            for field in fields:
                if not columns_to_be_cleaned[i]:
                    cleaned_row +=field+';'
                i+=1
            #print(cleaned_row)
            yield cleaned_row+'\n'


def main():
    global first
    config = configparser.RawConfigParser()
    config.read('clean_columns.cfg')
    columns = config.get('general', 'comma_separated_columns').split(',')
    import glob
    for kuksa_file_csv in glob.glob('csv_tiedostot\\*.csv'):
        with open('cleaned_csv\\{0}_kuukausi.csv'.format(os.path.splitext(os.path.basename(kuksa_file_csv))[0]), 'w') as cleaned_file:
            for cleaned_row in read_and_clean_kuksa_file(columns, kuksa_file_csv):
                cleaned_file.write(cleaned_row)
        cleaned_file.close()
        first=True

if __name__ == "__main__":
    #csv_from_excel('excelit//hp_liittyneet_2014-2015.xlsx', 'Sheet1')

    main()