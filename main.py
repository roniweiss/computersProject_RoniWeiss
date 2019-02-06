import matplotlib.pyplot as plt

def check_rows(data):
# in case of data in rows - organizes data in a dictionary and returns it.
# also looks for errors - if there's an error, prints the relevant one and stops running.
    dic = {}
    second_axis = data[-1]
    second_axis_list = second_axis.strip().split(': ')
    dic[second_axis_list[0]] = second_axis_list[1]
    data.remove(second_axis)
    first_axis = data[-1]
    first_axis_list = first_axis.strip().split(': ')
    dic[first_axis_list[0]] = first_axis_list[1]
    data.remove(first_axis)
    empty_line = data[-1]
    data.remove(empty_line)
    first_line_list = data[0].strip().split(' ')
    line_length = len(first_line_list)
    for line in data:
        line_list = line.lower().strip().split(' ')
        if len(line_list) != line_length:
            return "Input file error: Data lists are not the same length."
        if line_list[0] == 'x':
            dic['x'] = line_list[1:]
        if line_list[0] == 'dx':
            for i in range(1, len(line_list)):
                if float(line_list[i])<=0:
                    return "Input file error: Not all uncertainties are positive."
            dic['dx'] = line_list[1:]
        if line_list[0] == 'y':
            dic['y'] = line_list[1:]
        if line_list[0] == 'dy':
            for i in range(1, len(line_list)):
                if float(line_list[i])<=0:
                    return "Input file error: Not all uncertainties are positive."
            dic['dy'] = line_list[1:]
    return dic

def check_cols(data_list):
# in case of data in columns - organizes data in a dictionary and returns it.
# also looks for errors - if there's an error, prints the relevant one and stops running.
    dic = {}
    second_axis = data_list[-1]
    second_axis_list = second_axis.strip().split(': ')
    dic[second_axis_list[0]] = second_axis_list[1]
    data_list.remove(second_axis)
    first_axis = data_list[-1]
    first_axis_list = first_axis.strip().split(': ')
    dic[first_axis_list[0]] = first_axis_list[1]
    data_list.remove(first_axis)
    empty_line = data_list[-1]
    data_list.remove(empty_line)
    names_of_variables = data_list[0].lower().strip().split(' ')
    data_list.remove(data_list[0])
    first_list = []
    second_list = []
    third_list = []
    forth_list = []
    try:
        for line in data_list:
            line_list = line.strip().split(' ')
            first_list.append(line_list[0])
            second_list.append(line_list[1])
            third_list.append(line_list[2])
            forth_list.append(line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    dic[names_of_variables[0]] = first_list
    dic[names_of_variables[1]] = second_list
    dic[names_of_variables[2]] = third_list
    dic[names_of_variables[3]] = forth_list
    dx_values = dic['dx']
    dy_values = dic['dy']
    for index in range(len(first_list)):
        if float(dx_values[index])<=0 or float(dy_values[index])<=0:
            return "Input file error: Not all uncertainties are positive."
    return dic

def check_rows_or_cols(data_list):
# checks if data is in rows or columns.
# returns organized data in a dictionary (if data is valid).
    first_row = data_list[0].lower().strip().split(' ')
    if first_row[1][0] == 'd' or first_row[1][0] == 'y' or first_row[1][0] == 'x':
        return check_cols(data_list)
    else:
        return check_rows(data_list)

def make_dic_float(data_dic_string):
# creates a new dictionary containing the same data but with numbers as floats.
    new_dic = {}
    x_string_list = data_dic_string['x']
    y_string_list = data_dic_string['y']
    dx_string_list = data_dic_string['dx']
    dy_string_list = data_dic_string['dy']
    x_float_list=[]
    y_float_list=[]
    dx_float_list=[]
    dy_float_list=[]
    for index in range(len(x_string_list)):
        x_float_list.append(float(x_string_list[index]))
        y_float_list.append(float(y_string_list[index]))
        dx_float_list.append(float(dx_string_list[index]))
        dy_float_list.append(float(dy_string_list[index]))
    new_dic['x'] = x_float_list
    new_dic['y'] = y_float_list
    new_dic['dx'] = dx_float_list
    new_dic['dy'] = dy_float_list
    new_dic['x axis'] = data_dic_string['x axis']
    new_dic['y axis'] = data_dic_string['y axis']
    return new_dic

def calculate_fit_parameters(data_dic):
# calculates and returns the evaluated fitting parameters.
    x_values = data_dic['x']
    y_values = data_dic['y']
    dy_values = data_dic['dy']
    length=len(x_values)
    def calculate_avg(values,dys):
    # calculates and returns the average (according to instructions) of a given argument.
        sum = 0
        sum_dys = 0
        for index in range(length):
            temp_value = (values[index])/(dys[index]**2)
            sum += temp_value
            sum_dys += 1/(dys[index]**2)
        avg = sum/sum_dys
        return avg

    def calculate_sq_avg(values,dys):
    # calculates and returns the average of the squared value of a given argument.
        sum = 0
        sum_dys = 0
        for index in range(length):
            temp_value = values[index]
            sq_temp_value = (temp_value**2)/(dys[index]**2)
            sum += sq_temp_value
            sum_dys += 1/(dys[index]**2)
        sq_avg = sum/sum_dys
        return sq_avg

    def calculate_xy_avg(values1, values2, dys):
    # calculates and returns the average value of x and y product.
        sum_xys = 0
        sum_dys = 0
        for index in range(length):
            xy = (values1[index]*values2[index])/(dys[index]**2)
            sum_xys += xy
            sum_dys += 1/(dys[index]**2)
        xy_avg = sum_xys / sum_dys
        return xy_avg

    def calculate_chi_squared (data_dic):
    # calculates and returns the value of chi squared.
        sum_chi_sq = 0
        for index in range(length):
            y_value = data_dic['y'][index]
            x_value = data_dic['x'][index]
            dy_value = data_dic['dy'][index]
            temp_value = ((y_value-(a*x_value+b))/dy_value)**2
            sum_chi_sq += temp_value
        return sum_chi_sq

    x_avg = calculate_avg(x_values,dy_values)
    y_avg = calculate_avg(y_values,dy_values)
    dy_sq_avg = calculate_sq_avg(dy_values,dy_values)
    x_sq_avg = calculate_sq_avg(x_values,dy_values)
    xy_avg = calculate_xy_avg(x_values, y_values,dy_values)
    sum_dys = 0
    for index in range (length):
        sum_dys += dy_values[index]
    x_avg_sq = x_avg**2
    a = (xy_avg-x_avg*y_avg)/(x_sq_avg-x_avg_sq)
    da = (dy_sq_avg/(length*(x_sq_avg-x_avg_sq)))**0.5
    b = y_avg-a*x_avg
    db = ((dy_sq_avg*x_sq_avg)/(length*(x_sq_avg-x_avg_sq)))**0.5
    chi_sq = calculate_chi_squared(data_dic)
    chi_sq_red = chi_sq/(length-2)
    return [a, da, b, db, chi_sq, chi_sq_red]

def find_x_min_and_max(dic):
# finds and returns min and max values for x in data.
    x_min = dic['x'][0]
    x_max = dic['x'][0]
    x_values = dic['x']
    for value in x_values:
        if value<x_min:
            x_min = value
        if value>x_max:
            x_max = value
    return [x_min,x_max]

def calculate_y_min_and_max(x_min_and_max,linear_fit_list):
# finds y values according to y=ax+b.
# returns min and max values for y (in order to plot the linear fit).
    a = linear_fit_list[0]
    b = linear_fit_list[2]
    y_min = a*(x_min_and_max[0])+b
    y_max = a*(x_min_and_max[1])+b
    return [y_min,y_max]

def linear_plot(data_dic_string, linear_fit_values):
# plots and saves the linear fit.
    dic = make_dic_float(data_dic_string)
    x_min_and_max_values = find_x_min_and_max(dic)
    y_min_and_max_values = calculate_y_min_and_max(x_min_and_max_values,linear_fit_values)
    x = dic['x']
    y = dic['y']
    dx = dic['dx']
    dy = dic['dy']
    x_axis = dic['x axis']
    y_axis = dic['y axis']
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor="blue", barsabove=True)
    plt.plot(x_min_and_max_values, y_min_and_max_values, 'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')

# main program:
def fit_linear(filename):
# calls the relevant functions and prints values of a, b, chi2, chi2reduced.
    opened_file = open(filename, 'r')
    data = opened_file.readlines()
    data_dic = check_rows_or_cols(data)
    if type(data_dic) == str:
        print(data_dic)
    else:
        data_dic=make_dic_float(data_dic)
        fit_parameters = calculate_fit_parameters(data_dic)
        print ('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.
               format(fit_parameters[0], fit_parameters[1], fit_parameters[2],
                      fit_parameters[3], fit_parameters[4], fit_parameters[5]))
        linear_plot(data_dic,fit_parameters)
    opened_file.close()

#from now on - bonus:
def bonus_check_rows(data):
# in case of data in rows - organizes data in a dictionary and returns it.
# also looks for errors - if there's an error, prints the relevant one and stops running.
    dic = {}
    b_data = data[-1]
    b_data_list = b_data.lower().strip().split(' ')
    dic[b_data_list[0]] = b_data_list[1],\
                                b_data_list[2], b_data_list[3]
    data.remove(b_data)
    a_data = data[-1]
    a_data_list = a_data.lower().strip().split(' ')
    dic[a_data_list[0]] = a_data_list[1],\
                                a_data_list[2], a_data_list[3]
    data.remove(a_data)
    data = data[:-1]
    x_axis = data[-2]
    x_axis_list = x_axis.strip().split(': ')
    dic[x_axis_list[0]] = x_axis_list[1]
    data.remove(x_axis)
    y_axis = data[-1]
    y_axis_list = y_axis.strip().split(': ')
    dic[y_axis_list[0]] = y_axis_list[1]
    data.remove(y_axis)
    data = data[:-1]
    first_line_list = data[0].strip().split(' ')
    line_length = len(first_line_list)
    for line in data:
        line_list = line.lower().strip().split(' ')
        if len(line_list) != line_length:
            return "Input file error: Data lists are not the same length."
        if line_list[0] == 'x':
            dic['x'] = line_list[1:]
        if line_list[0] == 'dx':
            for index in range(1, len(line_list)):
                if float(line_list[index])<=0:
                    return "Input file error: Not all uncertainties are positive."
            dic['dx'] = line_list[1:]
        if line_list[0] == 'y':
            dic['y'] = line_list[1:]
        if line_list[0] == 'dy':
            for index in range(1, len(line_list)):
                if float(line_list[index])<=0:
                    return "Input file error: Not all uncertainties are positive."
            dic['dy'] = line_list[1:]
    return dic

def bonus_check_cols(data):
# in case of data in columns - organizes data in a dictionary and returns it.
# also looks for errors - if there's an error, prints the relevant one and stops running.
    dic = {}
    b_data = data[-1]
    b_data_list = b_data.lower().strip().split(' ')
    dic[b_data_list[0]] = b_data_list[1],\
                                b_data_list[2], b_data_list[3]
    data.remove(b_data)
    a_data = data[-1]
    a_data_list = a_data.lower().strip().split(' ')
    dic[a_data_list[0]] = a_data_list[1],\
                                a_data_list[2], a_data_list[3]
    data.remove(a_data)
    data = data[:-1]
    x_axis = data[-2]
    x_axis_list = x_axis.strip().split(': ')
    dic[x_axis_list[0]] = x_axis_list[1]
    data.remove(x_axis)
    y_axis = data[-1]
    y_axis_list = y_axis.strip().split(': ')
    dic[y_axis_list[0]] = y_axis_list[1]
    data.remove(y_axis)
    empty_line = data[-1]
    data.remove(empty_line)
    names_of_variables = data[0].lower().strip().split(' ')
    data.remove(data[0])
    first_list = []
    second_list = []
    third_list = []
    forth_list = []
    try:
        for line in data:
            line_list = line.strip().split(' ')
            first_list.append(line_list[0])
            second_list.append(line_list[1])
            third_list.append(line_list[2])
            forth_list.append(line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    dic[names_of_variables[0]] = first_list
    dic[names_of_variables[1]] = second_list
    dic[names_of_variables[2]] = third_list
    dic[names_of_variables[3]] = forth_list
    dx_values = dic['dx']
    dy_values = dic['dy']
    for index in range(len(first_list)):
        if float(dx_values[index])<=0 or float(dy_values[index])<=0:
            return "Input file error: Not all uncertainties are positive."
    return dic

def bonus_check_rows_or_cols(data_list):
# checks if data is in rows or columns.
# returns organized data in a dictionary (if data is valid).
    first_row = data_list[0].lower().strip().split(' ')
    if first_row[1][0] == 'x' or first_row[1][0] == 'y' or first_row[1][0] == 'd':
       return bonus_check_cols(data_list)
    else:
        return bonus_check_rows(data_list)

def calculate_temp_chi(a, b, data_dic):
# calculates initial chi squared value.
    temp_chi_squared = 0
    for index in range(len(data_dic['x'])):
        xi = data_dic['x'][index]
        xi_plus_dx = xi + data_dic['dx'][index]
        xi_minus_dx = xi - data_dic['dx'][index]
        yi = data_dic['y'][index]
        dyi = data_dic['dy'][index]
        temp_value = ((yi-(a*xi+b))/(((dyi)**2+((a*xi_plus_dx+b-(a*xi_minus_dx+b)))**2)** 0.5))
        temp_chi_squared += (temp_value**2)
    return temp_chi_squared

def calculate_chi_sq(data_dic):
# finds the min chi squared.
# returns a list with a, da, b, db of the min chi squared and min chi squared itself.
    min_a = min(data_dic['a'][0], data_dic['a'][1])
    max_a = max(data_dic['a'][0], data_dic['a'][1])
    step_a = abs(data_dic['a'][2])
    min_b = min(data_dic['b'][0], data_dic['b'][1])
    max_b = max(data_dic['b'][0], data_dic['b'][1])
    step_b = abs(data_dic['b'][2])
    min_chi = calculate_temp_chi(min_a, min_b, data_dic)
    chi_min_a = min_a
    chi_min_b = min_b
    b = min_b
    while b<=max_b:
        a = min_a
        while a<=max_a:
            temp_chi = calculate_temp_chi(a, b, data_dic)
            if temp_chi<min_chi:
                min_chi = temp_chi
                chi_min_a = a
                chi_min_b = b
            a += step_a
        b += step_b
    return [chi_min_a, step_a, chi_min_b, step_b, min_chi]

def calculate_as_and_chis_for_min_b(data_dic, min_b):
#finds a and chi squared values for the second bonus graph.
    min_a = min(data_dic['a'][0], data_dic['a'][1])
    max_a = max(data_dic['a'][0], data_dic['a'][1])
    step_a = abs(data_dic['a'][2])
    a_list = []
    chi_list = []
    a = min_a
    while a<=max_a:
        a_list.append(a)
        corr_chi = calculate_temp_chi(a, min_b, data_dic)
        chi_list.append(corr_chi)
        a+=step_a
    return [a_list,chi_list]

def numeric_sampling_plot(as_and_chis, min_b):
# plots and saves the second bonus fit - chi squared as a function of a (for min b).
    plt.clf()
    x = as_and_chis[0]
    y = as_and_chis[1]
    plt.plot(x, y)
    plt.xlabel('a')
    min_b_rounded = str(round(min_b,2))
    plt.ylabel("chi2(a,b="+min_b_rounded+")")
    plt.savefig('numeric_sampling.svg', bbox_inches='tight')

def make_bonus_dic_float(data_dic_string):
# creates a new dictionary containing the same data but with numbers as floats.
    new_dic = {}
    x_string_list = data_dic_string['x']
    y_string_list = data_dic_string['y']
    dx_string_list = data_dic_string['dx']
    dy_string_list = data_dic_string['dy']
    a_string_list = data_dic_string['a']
    b_string_list = data_dic_string['b']
    x_float_list = []
    y_float_list = []
    dx_float_list = []
    dy_float_list = []
    a_float_list = []
    b_float_list = []
    for index in range(len(x_string_list)):
        x_float_list.append(float(x_string_list[index]))
        y_float_list.append(float(y_string_list[index]))
        dx_float_list.append(float(dx_string_list[index]))
        dy_float_list.append(float(dy_string_list[index]))
    new_dic['x'] = x_float_list
    new_dic['y'] = y_float_list
    new_dic['dx'] = dx_float_list
    new_dic['dy'] = dy_float_list
    for value in a_string_list:
        a_float_list.append(float(value))
    new_dic['a']=a_float_list
    for value in b_string_list:
        b_float_list.append(float(value))
    new_dic['b'] = b_float_list
    new_dic['x axis']=data_dic_string['x axis']
    new_dic['y axis'] = data_dic_string['y axis']
    return new_dic

def bonus_linear_plot(data_dic, fit_parameters):
# plots and saves the first bonus fit.
    x_min_and_max = find_x_min_and_max(data_dic)
    y_min_and_max = []
    for x_value in x_min_and_max:
        y_value = x_value*fit_parameters[0]+fit_parameters[2]
        y_min_and_max.append(y_value)
    x = data_dic['x']
    y = data_dic['y']
    dx = data_dic['dx']
    dy = data_dic['dy']
    x_axis = data_dic['x axis']
    y_axis = data_dic['y axis']
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor='blue', barsabove=True)
    plt.plot(x_min_and_max, y_min_and_max, 'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')

#main bonus program:
def search_best_parameter(filename):
# calls the relevant functions and prints values of a, b, chi2, chi2reduced.
    plt.clf()
    opened_file = open(filename, 'r')
    data = opened_file.readlines()
    data_dic = bonus_check_rows_or_cols(data)
    if type(data_dic) == str:
        print(data_dic)
    else:
        data_dic = make_bonus_dic_float(data_dic)
        fit_parameters = calculate_chi_sq(data_dic)
        chi_sq_red = fit_parameters[4]/((len(data_dic['x']))-2)
        fit_parameters.append(chi_sq_red)
        print ('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.
               format(fit_parameters[0], fit_parameters[1], fit_parameters[2],
                      fit_parameters[3], fit_parameters[4], fit_parameters[5]))
        bonus_linear_plot(data_dic,fit_parameters)
        graph_parameters = calculate_as_and_chis_for_min_b(data_dic, fit_parameters[2])
        numeric_sampling_plot(graph_parameters, fit_parameters[2])
    opened_file.close()


