# generates plots and reports based off csv files from the Octet-BLI
#
# v0.1 2020-06-30
# Nicholas Lorig-Roach

import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import pandas as pd

# load style for matplotlib
plt.style.use('basic.mplstyle')

# set figure and panel sizes
fig_width = 7.5
fig_height = 10

panel_width = 2/fig_width
panel_height = 0.7/fig_height
plt.figure(1)

def prep_panels():
    ## text panels
    space = 1.0/8.2
    top = 0.9
    text1 = plt.axes([0.05, top, panel_width, panel_height])
    text2 = plt.axes([0.05, top-space*1, panel_width, panel_height])
    text3 = plt.axes([0.05, top-space*2, panel_width, panel_height])
    text4 = plt.axes([0.05, top-space*3, panel_width, panel_height])
    text5 = plt.axes([0.05, top-space*4, panel_width, panel_height])
    text6 = plt.axes([0.05, top-space*5, panel_width, panel_height])
    text7 = plt.axes([0.05, top-space*6, panel_width, panel_height])
    text8 = plt.axes([0.05, top-space*7, panel_width, panel_height])
    text_panels = [text1, text2, text3, text4, text5, text6, text7, text8]
    """
    i = 0
    for ax in text_panels:
        left = 0.05
        bottom = 0.85 - i
        increment = 1.0 / (len(text_panels) + 1)
        ax = plt.axes([left, bottom, panel_width, panel_height]) 
        i = i - increment
    """
    ## plot panels
    top = 0.89
    #plot1 = plt.axes([0.5, 0.5, panel_width, panel_height])
    plot1 = plt.axes([0.5, top, panel_width, panel_height])
    plot2 = plt.axes([0.5, top-space*1, panel_width, panel_height])
    plot3 = plt.axes([0.5, top-space*2, panel_width, panel_height])
    plot4 = plt.axes([0.5, top-space*3, panel_width, panel_height])
    plot5 = plt.axes([0.5, top-space*4, panel_width, panel_height])
    plot6 = plt.axes([0.5, top-space*5, panel_width, panel_height])
    plot7 = plt.axes([0.5, top-space*6, panel_width, panel_height])
    plot8 = plt.axes([0.5, top-space*7, panel_width, panel_height])
    plot_panels = [plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8]
    
    return text_panels, plot_panels
"""
## ought to automate prep_panels() better...
i = 0
for ax in plot_panels:
    left = 0.05
    bottom = 0.85 - i
    increment = 1.0 / (len(text_panels) + 1)
    ax = plt.axes([left, bottom, panel_width, panel_height]) 
    i = i - increment
"""
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def remove_empty_cols(df):

    for label in df.columns[::-1]:
        #print(label)
        if label == " " :
            print("empty identifier")
            if df[label][1] == " ":
                print(df[label])
                print("first value also empty, deleting column")
                df = df.drop(label, axis = 1)
    print(df.columns)
    return df

def plot_vertical_lines(ax, ymin, ymax, xcoords = []):
    for x in xcoords:
        ax.plot([x, x], [ymin, ymax], '--', linewidth = 0.4, \
                alpha = 0.7, color = 'black')
    

def import_octet_csv(filename, header_pos, drop_row_num = 0, \
                     return_dropped_row = True, index = 0):
    try:
        df = pd.read_csv(filename, header = header_pos, index_col = index)
        # clean up weird stuff from octet output
        df = remove_empty_cols(df)
        if return_dropped_row is True:
            dropped_row = df.xs(df.index.values[0])
            df = df.drop(df.index[[drop_row_num]], axis = 0)
            return df, dropped_row
        ## DEBUG PRINTS
        print(df.index)
        print(df.columns)
        print("# of samples: {}".format(len(df.columns)))
        return df

    except Exception as e:
        eprint("bad input.  usage: {} your_file.csv".format(sys.argv[0]))
        eprint(sys.argv)
        eprint("error: {}".format(e))

## read file
filename = sys.argv[1]
assay, wells  = import_octet_csv(filename, 2)


"""
## collect metadata from 'data cycles' csv from Octet software
if sys.argv[2]:
    filename = sys.argv[2]
    metadata = import_octet_csv(filename, 0, return_dropped_row=False, \
                                index = 6)
    metadata = metadata.iloc[::2, :]
    print(metadata)
    filename = sys.argv[1].split("/")[-1].split(".")[0]
    metadata.to_csv('{}_metadata.csv'.format(filename))
"""
#######################################
### try some plotting  ################
#######################################

a1_results = []
a2_results = []
labels = []
##set assay timepoints
# with load
#b1, l1, a1_t0, a1_t1, a2_t0, a2_t1 = 60, 180, 240, 840, 900, 1200
b1, l1, a1_t0, a1_t1, a2_t0, a2_t1 = 60, 180, 240, 840, 900, 1080
# extra long load
#b1, l1, a1_t0, a1_t1, a2_t0, a2_t1 = 60, 660, 720, 1320, 1380, 1560

# no antigen loading step
#b1, l1, a1_t0, a1_t1, a2_t0, a2_t1 = 0, 60, 120, 720, 780, 1080
"""
b1 = 60
l1 = 180
a1_t0 = 240
a1_t1 = 840
a2_t0 = 900
a2_t1 = 1200
"""
## prepare panels for figure, atm prep_panels() is hard coded for 8 
text_panels, plot_panels = prep_panels()
num_panels = 8
page_number = 1
j = -1 # track how many graphs we've done per page, zero indexed
filename = sys.argv[1].split("/")[-1].split(".")[0]
print("filename {}".format(filename))

## iterate through each sample, plot QC graph and store association 
##    analyses
for i, (label, data) in enumerate(assay.items()):

    ## check if there's room for another panel, if not safe figure and 
    ##      make new page
    j = j + 1 
    if j + 1 > num_panels:
        # reset, save current page, initialize next page
        num_graphs = 0
        text_panels[0].text(0,1.3, sys.argv[1], va = 'top', ha = 'left', \
                            fontsize = 7)
        
        plt.savefig('{}_plots{}.png'.format(filename,page_number), \
                     dpi = 1200)
        page_number = 1 + int(i/num_panels) # int() does floor rounding
        plt.figure(page_number)
        text_panels, plot_panels = prep_panels()
    
    ## temp assay step time dileanation change due to loading time 
    ##    differences in 061520 octet data
    #if i is 16:
    #    b1, l1, a1_t0, a1_t1, a2_t0, a2_t1 = 60, 180, 240, 840, 900, 1080
    
    ## PLOTS
    data = pd.to_numeric(data)
    x = data.index.values
    x = pd.to_numeric(x) #indices didn't get converted by above to_numeric
    y = data.values
    plot_panels[j].plot(x, y, linewidth = 0.6)
    
    ## TEXT & STATS
    text_panels[j].set_axis_off()
    text_panels[j].set_frame_on(False)
    text_panels[j].text(0,1, "{}    well {}".format(label, wells[i]), \
                        va = 'top', ha = 'left', fontsize = 8)
    
    timestep = x[1] - x[0]
    timerange = 5
    
    ymin, ymax = np.amin(y), np.amax(y) + 0.25
    ## draw octet step demarcations / lines
    plot_vertical_lines(plot_panels[j], ymin, ymax, \
                           [b1, l1, a1_t0, a1_t1, a2_t0, a2_t1])
    

    # baseline2 = avg of seconds 2-4 of assoc 1
    t0 = int((a1_t0 + 2) / timestep) - 1
    t1 = int((a1_t0 + 4) / timestep) - 1
    baseline2 = np.average(y[t0:t1])
    text_panels[j].text(0,0.6, 'Baseline2 (avg between {} and {} sec): {:.2f}'.format(x[t0], x[t1], baseline2), va = 'top', ha = 'left', fontsize = 5)
    plot_panels[j].plot([x[t0], x[t1]], [y[t0], y[t1]],  \
                    linewidth = 0.8,  alpha = 0.7, color = 'red')

    # assoc1 set as last 5 sec of association step 
    t0 = int((a1_t1 - 5) / timestep) - 1
    t1 = int(a1_t1/ timestep) - 1
    load2 = np.average(y[t0:t1])
    text_panels[j].text(0,0.4, 'Assoc1 (avg between {} and {} sec): {:.2f}'.format(x[t0], x[t1], load2), va = 'top', ha = 'left', fontsize = 5)
    text_panels[j].text(1.1,0.4, '$\Delta$2 = {:.4f}'.format(load2-baseline2), va = 'top', ha = 'left', fontsize = 5)
    plot_panels[j].plot([x[t0], x[t1]], [y[t0], y[t1]],  \
                    linewidth = 0.8,  alpha = 0.7, color = 'red')



    # baseline3 = seconds 2-4 of assoc 2
    t0 = int((a2_t0 + 2) / timestep) - 1
    t1 = int((a2_t0 + 4) / timestep) - 1
    baseline3 = np.average(y[t0:t1])
    text_panels[j].text(0,0.2, 'Baseline3 (avg between {} and {} sec): {:.2f}'.format(x[t0], x[t1], baseline3), va = 'top', ha = 'left', fontsize = 5)
    plot_panels[j].plot([x[t0], x[t1]], [y[t0], y[t1]],  \
                    linewidth = 0.8,  alpha = 0.7, color = 'red')

    # assoc2 = last 5 seconds of step
    t0 = int((a2_t1 -5) / timestep) - 1
    t1 = int(a2_t1 / timestep) - 1
    load3 = np.average(y[t0:t1])
    text_panels[j].text(0,0.0, 'Assoc2 (avg between {} and {} sec): {:.2f}'.format(x[t0], x[t1], load3), va = 'top', ha = 'left', fontsize = 5)
    text_panels[j].text(1.1,0.0, '$\Delta$3 = {:.4f}'.format(load3-baseline3), va = 'top', ha = 'left', fontsize = 5)
    plot_panels[j].plot([x[t0], x[t1]], [y[t0], y[t1]],  \
                    linewidth = 0.8,  alpha = 0.7, color = 'red')

    labels.append(label)
    a1_results.append(load2-baseline2)
    a2_results.append(load3-baseline3)


## finish and save last page
text_panels[0].text(0,1.3, sys.argv[1], 
                                va = 'top', ha = 'left', fontsize = 7)

plt.savefig('{}_plots{}.png'.format(filename,page_number), dpi = 1200)

## save a csv file with the calculated values from association 1 and 2
filename_list = [filename] * len(labels)
data = pd.DataFrame( \
        list(zip(filename_list, labels, wells, a1_results, a2_results)),\
            columns = ['Batch','Octet file', 'Well', 'Assoc1', 'Assoc2'])

data.to_csv('{}_data.csv'.format(filename))
