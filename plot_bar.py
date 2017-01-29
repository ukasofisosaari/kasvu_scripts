import plotly as py
import plotly.graph_objs as go
import glob
import os


def main_plotly(generate_city_data, kuksa_file_csv):
    new_members_for_disctrict = 0
    kotikunta = 0
    empty_field = 0
    no_sex = 0
    data_structure = {2014: {}, 2015: {}}
    #This for the whole group(piiri)
    district_whole_year = {2014:{},
                           2015:{}
                           }
    scout_district =  {2014: {}, 2015: {}}
    with open(kuksa_file_csv, 'r') as cleaned_file:
        for row in cleaned_file:
            fields = row.split(';')
            if 'Kotikunta' not in fields and 'Ei tietoa' not in fields and '' not in fields:
                city = fields[0]
                vuosi = int(fields[0].split('.')[2])
                kuukausi = int(fields[0].split('.')[1])
                if vuosi > 2013 and vuosi < 2016:
                    sex = fields[2]
                    age_group=''
                    joining_age = vuosi-int(fields[3])
                    if joining_age < 10:
                        age_group = 'Sudenpennut (7-9 v)'
                    elif 9 < joining_age < 12:
                        age_group = 'Seikkailijat (10-11 v)'
                    elif 11 < joining_age < 15:
                        age_group = 'Tarpojat (12-14 v)'
                    elif 14 < joining_age < 18:
                        age_group = 'Samoajat (15-17 v)'
                    elif 17 < joining_age < 23:
                        age_group = 'Vaeltajat (18-22 v)'
                    elif joining_age > 22:
                        age_group = 'Aikuiset'
                    else:
                        print('Age does not fit into limits: {0}'.format(str(joining_age)))
                    #First count for whole scout district and add into data structure
                    try:
                        district_sexes = scout_district[vuosi][kuukausi]
                    except KeyError:
                        district_sexes = {}
                        scout_district[vuosi][kuukausi] = district_sexes
                        district_whole_year[vuosi][kuukausi] = {}

                    try:
                        disctrict_age_groups = district_sexes[sex]
                    except KeyError:
                        disctrict_age_groups = {'Aikuiset':0, 'Samoajat (15-17 v)':0, 'Seikkailijat (10-11 v)':0, 'Sudenpennut (7-9 v)':0, 'Tarpojat (12-14 v)':0, 'Vaeltajat (18-22 v)':0}
                        district_whole_year[vuosi][kuukausi][sex] = 0
                    disctrict_age_groups[age_group] += 1
                    district_sexes[sex] =  disctrict_age_groups
                    district_whole_year[vuosi][kuukausi][sex] += 1
                    #Then per city
                    try:
                         cities = data_structure[vuosi][kuukausi]
                    except KeyError:
                         cities = {}
                         data_structure[vuosi][kuukausi] = cities

                    try:
                        sexes = cities[city]
                    except KeyError:
                        sexes = {}
                        data_structure[city] = sexes

                    try:
                        age_groups = sexes[sex]
                    except KeyError:
                        age_groups = {'Aikuiset':0, 'Samoajat (15-17 v)':0, 'Seikkailijat (10-11 v)':0, 'Sudenpennut (7-9 v)':0, 'Tarpojat (12-14 v)':0, 'Vaeltajat (18-22 v)':0}

                    age_groups[age_group] += 1
                    sexes[sex] = age_groups

            elif 'Kotikunta' in fields:
                kotikunta +=1
            elif 'Ei tietoa' in fields:
                no_sex += 1
            elif '' in fields:
                empty_field += 1
            else:
                print(fields)

    for vuosi in scout_district.keys():
        district_whole_year
        x_girls = []
        y_girls= []
        for kuukausi in district_whole_year[vuosi].keys():
            new_members_for_disctrict += district_whole_year[vuosi][kuukausi]['Nainen']
            x_girls.append(kuukausi)
            y_girls.append(district_whole_year[vuosi][kuukausi]['Nainen'])

        girls = go.Bar(
            x= x_girls,
            y=y_girls,
            name='Tytöt'
        )

        x_boys = []
        y_boys= []
        for kuukausi in district_whole_year[vuosi].keys():
            new_members_for_disctrict += district_whole_year[vuosi][kuukausi]['Mies']
            x_boys.append(kuukausi)
            y_boys.append(district_whole_year[vuosi][kuukausi]['Mies'])
        boys = go.Bar(
            x=x_boys,
            y=y_boys,
            name='Pojat'
        )
        data = [girls, boys]
        layout = go.Layout(barmode='group', title='HP liittyneet partiolaiset {0}'.format(  vuosi))
        fig = go.Figure(data=data, layout=layout)
        html_filename = 'graphs/piiri_{0}.html'.format( vuosi)
        py.offline.plot(fig, filename=html_filename, auto_open=False)

        joiners_by_age_groups = {'Nainen':{}, 'Mies':{}}
        joiners_by_age_groups_in_cities ={}

        for kuukausi in scout_district[vuosi]:
            x_girls = []
            y_girls= []
            for age_group in scout_district[vuosi][kuukausi]['Nainen'].keys():
                new_members_for_disctrict += scout_district[vuosi][kuukausi]['Nainen'][age_group]
                x_girls.append(age_group)
                y_girls.append(scout_district[vuosi][kuukausi]['Nainen'][age_group])
                try:
                    joiners_by_age_groups['Nainen'][age_group] +=scout_district[vuosi][kuukausi]['Nainen'][age_group]
                except:
                    joiners_by_age_groups['Nainen'][age_group] = scout_district[vuosi][kuukausi]['Nainen'][age_group]


            girls = go.Bar(
                x= x_girls,
                y=y_girls,
                name='Tytöt'
            )

            x_boys = []
            y_boys= []
            for age_group in scout_district[vuosi][kuukausi]['Mies'].keys():
                new_members_for_disctrict += scout_district[vuosi][kuukausi]['Mies'][age_group]
                x_boys.append(age_group)
                y_boys.append(scout_district[vuosi][kuukausi]['Mies'][age_group])

                try:
                    joiners_by_age_groups['Mies'][age_group] +=scout_district[vuosi][kuukausi]['Mies'][age_group]
                except:
                    joiners_by_age_groups['Mies'][age_group] = scout_district[vuosi][kuukausi]['Mies'][age_group]

            boys = go.Bar(
                x=x_boys,
                y=y_boys,
                name='Pojat'
            )
            data = [girls, boys]
            layout = go.Layout(barmode='group', title='HP liittyneet partiolaiset {0} {1}'.format( kuukausi, vuosi))
            fig = go.Figure(data=data, layout=layout)
            html_filename = 'graphs/piiri_{0}_{1}.html'.format(kuukausi, vuosi)
            py.offline.plot(fig, filename=html_filename, auto_open=False)
            print(empty_field)
            print(new_members_for_disctrict)

            if generate_city_data:
                print("Generating city data")
                print(data_structure)
                exit()
                for city in data_structure[vuosi][kuukausi].keys():
                    print("City")
                    joiners_by_age_groups_in_cities[city] = {'Nainen':{}, 'Mies':{}}
                    x_girls = []
                    y_girls= []
                    try:
                        for age_group in data_structure[city]['Nainen'].keys():
                            x_girls.append(age_group)
                            y_girls.append(data_structure[city]['Nainen'][age_group])
                            try:
                                joiners_by_age_groups_in_cities[city]['Nainen'][age_group] += joiners_by_age_groups_in_cities[city]['Nainen'][age_group]
                            except:
                                joiners_by_age_groups_in_cities[city]['Nainen'][age_group] = joiners_by_age_groups_in_cities[city]['Nainen'][age_group]

                    except KeyError:
                        pass

                    girls = go.Bar(
                        x= x_girls,
                        y=y_girls,
                        name='Tytöt'
                    )

                    x_boys = []
                    y_boys= []
                    try:
                        for age_group in data_structure[city]['Mies'].keys():
                            x_boys.append(age_group)
                            y_boys.append(data_structure[city]['Mies'][age_group])
                            try:
                                joiners_by_age_groups_in_cities[city]['Mies'][age_group] += joiners_by_age_groups_in_cities[city]['Mies'][age_group]
                            except:
                                joiners_by_age_groups_in_cities[city]['Mies'][age_group] = joiners_by_age_groups_in_cities[city]['Mies'][age_group]
                    except KeyError:
                        pass
                    boys = go.Bar(
                        x=x_boys,
                        y=y_boys,
                        name='Pojat'
                    )
                    data = [girls, boys]
                    layout = go.Layout(barmode='group', title='{0} liittyneet partiolaiset {1} {2}'.format(city, kuukausi, vuosi))
                    fig = go.Figure(data=data, layout=layout)
                    try:
                        os.makedirs('graphs/{0}/'.format(city))
                    except FileExistsError:

                        pass
                    py.offline.plot(fig, filename='graphs/{2}/piiri_{0}_{1}.html'.format(kuukausi, vuosi, city), auto_open=False)
        district_plot_joiners_age_group_year(vuosi, joiners_by_age_groups)
        if generate_city_data:
            cities_plot_joiners_age_group_year(vuosi, joiners_by_age_groups_in_cities)

def cities_plot_joiners_age_group_year(vuosi, joiners_by_age_groups_in_cities):
   for city in joiners_by_age_groups_in_cities.keys():
        x_girls = []
        y_girls= []
        for age_group in joiners_by_age_groups_in_cities[city]['Nainen'].keys():
            x_girls.append(age_group)
            y_girls.append(joiners_by_age_groups_in_cities[city]['Nainen'][age_group])
        girls = go.Bar(
            x= x_girls,
            y=y_girls,
            name='Tytöt'
        )

        x_boys = []
        y_boys= []
        for age_group in joiners_by_age_groups_in_cities[city]['Mies'].keys():
            x_boys.append(age_group)
            y_boys.append(joiners_by_age_groups_in_cities[city]['Mies'][age_group])

        boys = go.Bar(
            x=x_boys,
            y=y_boys,
            name='Pojat'
        )
        data = [girls, boys]
        layout = go.Layout(barmode='group', title='HP liittyneet partiolaiset {1} {0}'.format( vuosi, city))
        fig = go.Figure(data=data, layout=layout)
        print('graphs/{1}/piiri_agegroup_joiners_{0}.html'.format( vuosi, city))
        html_filename = 'graphs/{1}/piiri_agegroup_joiners_{0}.html'.format( vuosi, city)
        py.offline.plot(fig, filename=html_filename, auto_open=False)

def district_plot_joiners_age_group_year(vuosi, joiners_by_age_groups):
    x_girls = []
    y_girls= []
    for age_group in joiners_by_age_groups['Nainen'].keys():
        x_girls.append(age_group)
        y_girls.append(joiners_by_age_groups['Nainen'][age_group])
    girls = go.Bar(
        x= x_girls,
        y=y_girls,
        name='Tytöt'
    )

    x_boys = []
    y_boys= []
    for age_group in joiners_by_age_groups['Mies'].keys():
        x_boys.append(age_group)
        y_boys.append(joiners_by_age_groups['Mies'][age_group])

    boys = go.Bar(
        x=x_boys,
        y=y_boys,
        name='Pojat'
    )
    data = [girls, boys]
    layout = go.Layout(barmode='group', title='HP liittyneet partiolaiset {0}'.format( vuosi))
    fig = go.Figure(data=data, layout=layout)
    html_filename = 'graphs/piiri_agegroup_joiners{0}.html'.format( vuosi)
    py.offline.plot(fig, filename=html_filename, auto_open=False)


def district_plot_joiners_age_group_year(vuosi, joiners_by_age_groups):
    x_girls = []
    y_girls= []
    for age_group in joiners_by_age_groups['Nainen'].keys():
        x_girls.append(age_group)
        y_girls.append(joiners_by_age_groups['Nainen'][age_group])
    girls = go.Bar(
        x= x_girls,
        y=y_girls,
        name='Tytöt'
    )

    x_boys = []
    y_boys= []
    for age_group in joiners_by_age_groups['Mies'].keys():
        x_boys.append(age_group)
        y_boys.append(joiners_by_age_groups['Mies'][age_group])

    boys = go.Bar(
        x=x_boys,
        y=y_boys,
        name='Pojat'
    )
    data = [girls, boys]
    layout = go.Layout(barmode='group', title='HP liittyneet partiolaiset {0}'.format( vuosi))
    fig = go.Figure(data=data, layout=layout)
    html_filename = 'graphs/piiri_agegroup_joiners{0}.html'.format( vuosi)
    py.offline.plot(fig, filename=html_filename, auto_open=False)







if __name__ == "__main__":

    main_plotly(True, 'cleaned_csv/hp_liittyneet_2014-2015.csv')