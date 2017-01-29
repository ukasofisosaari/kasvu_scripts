#This script uses selenium to fetch data from kuksa

import calendar
import os
import shutil
import xlrd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select



class KuksaFetch:
    selection_rows = ['[Kotikunta]','[Jäsenyyden alkamispäivä]','[Sukupuoli]','[Syntymävuosi]']
    def __init__(self, kuksa_address, user_name, pass_word, download_directory, log_file):
        self._username = user_name
        self._password = pass_word
        self._kuksa_address = kuksa_address
        self._log_file = log_file
        self._download_dir = download_directory
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir",download_directory)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self._browser = webdriver.Firefox(firefox_profile=fp)
        self._browser.get(kuksa_address)

        username = self._browser.find_element_by_name('username')
        username.send_keys(self._username)

        password = self._browser.find_element_by_name('password')
        password.send_keys(self._password)

        form = self._browser.find_element_by_name('sender')
        form.submit()


    def _log(self, log_str):
        with open(self._log_file, "a") as logFile:
            logFile.write(log_str+'\n')
        logFile.close()

    def set_selection_rows(self):
        b_selection_rows = self._browser.find_element_by_partial_link_text('Valitse sarakkeet')
        b_selection_rows.click()
        i = 1
        for selection_row in self.selection_rows:
            select = Select(self._browser.find_element_by_id('cphContent_ddSarake{0}_Drop'.format(str(i))))
            select.select_by_visible_text(selection_row)
            i+=1
        save = self._browser.find_element_by_id('cphContent_btnTallenna')
        save.click()

    def get_members_joined(self, vuosi_kuukaudet):
        try:
            shutil.rmtree('temp')
        except FileNotFoundError:
            pass
        poiminta = self._browser.find_element_by_partial_link_text('Poiminta')
        poiminta.click()

        self.set_selection_rows()

        os.makedirs('temp')
        for vuosi in vuosi_kuukaudet.keys():
            for kuukausi in vuosi_kuukaudet[vuosi]:

                poiminta = self._browser.find_element_by_id('cphContent_btnUusiPoiminta')
                poiminta.click()
                weekday, last = calendar.monthrange(vuosi, kuukausi)

                #Select henkilojasenet
                personal_members_cb = self._browser.find_element_by_id('cphContent_chkMyosPiirienLippukuntienJasenet')
                personal_members_cb.click()

                #Set dates for having joined
                first_possible_date_input = self._browser.find_element_by_id('cphContent_JASAlkupvm1')
                first_possible_date_input.send_keys('1.'+str(kuukausi)+'.'+str(vuosi))
                last_possible_date_input = self._browser.find_element_by_id('cphContent_JASAlkupvm2')
                last_possible_date_input.send_keys(str(last)+'.'+str(kuukausi)+'.'+str(vuosi))

                #Click poimi
                personal_members_cb = self._browser.find_element_by_id('cphContent_btnPoimi')
                personal_members_cb.click()

                #Click download excel
                personal_members_cb = self._browser.find_element_by_id('cphContent_lbtnExcel')
                personal_members_cb.click()
                excel_file='temp\\{0}_{1}.xlsx'.format(kuukausi, vuosi)
                try:
                    #Rename file
                    os.rename(self._download_dir+'Rautiainen', excel_file)
                except NoSuchElementException:
                    pass
                csv_filename = 'HP_liittyneet_{0}_{1}.csv'.format(kuukausi, vuosi)
                first_file = True
                with open('csv_tiedostot\\'+csv_filename, 'w') as csv_file:
                    try:
                        wb = xlrd.open_workbook(excel_file)
                        sh = wb.sheet_by_name('Sheet1')
                        for rownum in range(sh.nrows):
                            csv_row=';'
                            for value in sh.row_values(rownum):
                                #print(value)
                                csv_row += str(value)+';'
                            csv_row += '\n'
                            csv_file.write(csv_row)
                    except xlrd.biffh.XLRDError:
                        pass
                csv_file.close()
        shutil.rmtree('temp')

    def get_age_groups(self, sexes, age_groups):
        try:
            shutil.rmtree('temp')
        except FileNotFoundError:
            pass
        poiminta = self._browser.find_element_by_partial_link_text('Poiminta')
        poiminta.click()

        self.set_selection_rows()

        os.makedirs('temp')
        for sex in sexes:
            for age_group in age_groups:

                poiminta = self._browser.find_element_by_id('cphContent_btnUusiPoiminta')
                poiminta.click()

                #Select henkilojasenet
                personal_members_cb = self._browser.find_element_by_id('cphContent_chkMyosPiirienLippukuntienJasenet')
                personal_members_cb.click()

                #Select sex
                sex_select = Select(self._browser.find_element_by_id('cphContent_lbSukupuoli'))
                sex_select.select_by_visible_text(sex)

                #Select age_group
                age_group_select = Select(self._browser.find_element_by_id('cphContent_lbRyhmaIkakausi'))
                age_group_select.select_by_visible_text(age_group)

                #Click poimi
                personal_members_cb = self._browser.find_element_by_id('cphContent_btnPoimi')
                personal_members_cb.click()

                #Click download excel
                personal_members_cb = self._browser.find_element_by_id('cphContent_lbtnExcel')
                personal_members_cb.click()
                excel_file='temp\\{0}_{1}.xlsx'.format(sex, age_group)
                try:
                    #Rename file
                    os.rename(self._download_dir+'Rautiainen', excel_file)
                except NoSuchElementException:
                    pass
                csv_filename = 'HP_{0}_{1}.csv'.format(sex, age_group)
                first_file = True
                with open('csv_tiedostot\\'+csv_filename, 'w') as csv_file:
                    try:
                        wb = xlrd.open_workbook(excel_file)
                        sh = wb.sheet_by_name('Sheet1')
                        for rownum in range(sh.nrows):
                            csv_row=';'
                            for value in sh.row_values(rownum):
                                #print(value)
                                csv_row += str(value)+';'
                            csv_row += '\n'
                            csv_file.write(csv_row)
                    except xlrd.biffh.XLRDError:
                        pass
                csv_file.close()
        shutil.rmtree('temp')

def main():
    password=""
    username=""
    kuksa_address=""
    sexes = ['Mies', 'Nainen']
    age_groups = ['Aikuiset', 'Samoajat (15-17 v)', 'Seikkailijat (10-11 v)', 'Sudenpennut (7-9 v)', 'Tarpojat (12-14 v)', 'Vaeltajat (18-22 v)']
    log_file='C:\\Users\\ukas\\Documents\\Kasvuryhmä_data_louhinta\\kuksaFetch.log'
    download_dir = 'C:\\Users\\ukas\\Documents\\Kasvuryhmä_data_louhinta\\excelit\\'
    kuksa_fetch = KuksaFetch(kuksa_address, username, password, download_dir, log_file)
    kuksa_fetch.get_age_groups(sexes, age_groups)


if __name__ == "__main__":
    main()