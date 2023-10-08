import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plotter(app: object, eleana: object, comboboxLists: object):
    '''Ta funkcja zbiera informacje o wszystkich wyborach i wyswietla odpowiednie
    wartości na wykresie.
    Funkcje trzeba rozbudowac o elementy, które sprawdzają czy mamy wyświetlić
    część także część urojoną. Wtedy do wykresu dokładamy po jednej krzywej, np. przerywanej
    do każdego wybor FIRST, SECOND itd.

    Ostatecznie funkcja zostanie przeniesiona do innego pliku
    '''

    # Set colors for series in graph
    color_first_re = "#d53339"
    color_first_im = "#ef6f74"

    color_second_re = "#008cb3"
    color_second_im = "#07bbed"

    color_result_re = "#108d3d"
    color_result_im = "#32ab5d"

    first_complex = False
    second_complex = False
    result_complex = False

    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)

    # FIRST
    index = eleana.selections['first']

    if eleana.selections['f_dsp'] and index >= 0:
        data_for_plot = eleana.getDataFromSelection(eleana, 'first')
        data_index = eleana.selections['first']
        first_x = data_for_plot['x']
        first_complex = data_for_plot['complex']
        first_re_y = data_for_plot['re_y']
        first_im_y = data_for_plot['im_y']
        first_legend_index = eleana.selections['first']
        first_legend = eleana.dataset[first_legend_index].name
        print(first_re_y)
        # Label for x axis
        try:
            label_x_title = eleana.dataset[data_index].parameters['name_x']
        except:
            label_x_title = ''
        try:
            label_x_unit = eleana.dataset[data_index].parameters['unit_x']
        except:
            label_x_unit = 'a.u.'
        first_label_x = label_x_title + ' [' + label_x_unit + ']'

        # Labels for y axis
        try:
            label_y_title = eleana.dataset[data_index].parameters['name_y']
        except:
            label_y_title = ''
        try:
            label_y_unit = eleana.dataset[data_index].parameters['unit_y']
        except:
            label_y_unit = 'a.u.'
        first_label_y = label_y_title + ' [' + label_y_unit + ']'

    else:
        first_x = np.array([])
        first_re_y = np.array([])
        first_im_y = np.array([])
        first_legend = 'no plot'
        first_label_x = ''
        first_label_y = ''

    # Add FIRST to plot
    ax.set_ylabel(first_label_y)
    ax.set_xlabel(first_label_x)
    if first_complex:
        if eleana.selections['f_cpl'] == 'im':
            first_legend = first_legend + ' :IMAG'
            ax.plot(first_x, first_im_y, label=first_legend, color=color_first_im)
        elif eleana.selections['f_cpl'] == 'magn':
            first_legend = first_legend + ' :MAGN'
            ax.plot(first_x, first_re_y, label=first_legend, color=color_first_re)
        elif eleana.selections['f_cpl'] == 'cpl':
            first_legend_r = first_legend + ' :REAL'
            ax.plot(first_x, first_re_y, label=first_legend_r, color=color_first_re)
            first_legend_i = first_legend + ' :IMAG'
            ax.plot(first_x, first_im_y, label=first_legend_i, color=color_first_im)
        elif eleana.selections['f_cpl'] == 're':
            first_legend = first_legend + ' :REAL'
            ax.plot(first_x, first_re_y, label=first_legend, color=color_first_re)
    else:
        ax.plot(first_x, first_re_y, label=first_legend, color=color_first_re)

    # SECOND
    index = eleana.selections['second']

    if eleana.selections['s_dsp'] and index >=0:
        data_for_plot = eleana.getDataFromSelection(eleana, 'second')
        data_index = eleana.selections['second']
        second_x = data_for_plot['x']
        second_re_y = data_for_plot['re_y']
        second_im_y = data_for_plot['im_y']
        second_legend_index = eleana.selections['second']
        second_legend = eleana.dataset[second_legend_index].name

        # Label for x axis
        try:
            label_x_title = eleana.dataset[data_index].parameters['name_x']
        except:
            label_x_title = ''
        try:
            label_x_unit = eleana.dataset[data_index].parameters['unit_x']
        except:
            label_x_unit = 'a.u.'
        second_label_x = label_x_title + ' [' + label_x_unit + ']'

        # Labels for y axis
        try:
            label_y_title = eleana.dataset[data_index].parameters['name_y']
        except:
            label_y_title = ''
        try:
            label_y_unit = eleana.dataset[data_index].parameters['unit_y']
        except:
            label_y_unit = 'a.u.'
        second_label_y = label_y_title + ' [' + label_y_unit + ']'

    else:
        second_x = np.array([])
        second_re_y = np.array([])
        second_im_y = np.array([])
        second_legend = 'no plot'
        second_label_x = ''
        second_label_y = ''

    # Add SECOND to plot
    if eleana.selections['f_dsp'] and index >=0:
        # If FIRST spectrum is on then do not change axes labels
        pass
    else:
        # If FIRST spectrum is off or set tu None then change labels to those from SECOND
        ax.set_ylabel(second_label_y)
        ax.set_xlabel(second_label_x)

    ax.plot(second_x, second_re_y, label=second_legend, color=color_second_re)

    # RESULT
    if len(eleana.results_dataset) != 0:
        #index = comboboxLists.current_position(app, 'sel_result')['index']
        index = eleana.selections['first']

        if index != 0:
            is_result_not_none = True
        else:
            is_result_not_none = False

        if eleana.selections['s_dsp'] and is_result_not_none:
            data_for_plot = eleana.getDataFromSelection(eleana, 'result')
            data_index = eleana.selections['result']
            result_x = data_for_plot['x']
            result_re_y = data_for_plot['re_y']
            result_im_y = data_for_plot['im_y']
            result_legend_index = eleana.selections['result']
            result_legend = eleana.results_dataset[result_legend_index].name

            # Label for x axis
            try:
                label_x_title = eleana.results_dataset[data_index].parameters['name_x']
            except:
                label_x_title = ''
            try:
                label_x_unit = eleana.results_dataset[data_index].parameters['unit_x']
            except:
                label_x_unit = 'a.u.'
            result_label_x = label_x_title + ' [' + label_x_unit + ']'

            # Labels for y axis
            try:
                label_y_title = eleana.results_dataset[data_index].parameters['name_y']
            except:
                label_y_title = ''
            try:
                label_y_unit = eleana.results_dataset[data_index].parameters['unit_y']
            except:
                label_y_unit = 'a.u.'
            result_label_y = label_y_title + ' [' + label_y_unit + ']'

        else:
            result_x = np.array([])
            result_re_y = np.array([])
            result_im_y = np.array([])
            result_legend = 'no plot'
            result_label_x = ''
            result_label_y = ''

        # Add SECOND to plot
        if eleana.selections['f_dsp'] and eleana.selections['s_dsp'] and is_first_not_none and is_second_not_none:
            pass
        else:
            # If FIRST spectrum is off or set tu None then change labels to those from SECOND
            ax.set_ylabel(result_label_y)
            ax.set_xlabel(result_label_x)

        ax.plot(result_x, result_re_y, label=result_legend, color=color_result_re)

    # Put data on Graph
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=app.graphFrame)
    canvas.get_tk_widget().grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
    canvas.draw()
    app.graphFrame.columnconfigure(0, weight=1)
    app.graphFrame.rowconfigure(0, weight=1)

