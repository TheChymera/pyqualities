#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import numpy as np
import matplotlib.dates as mdates
import itertools
import pandas as pd
from matplotlib.pyplot import text
from scipy.stats import ttest_ind, sem
from os import path
from pylab import math, datetime, figure, tick_params, legend, xlabel, ylabel, title, matplotlib, show
from matplotlib import axis

remote_location ='http://chymera.eu/opendata/pyqualities/Christian_pyqualities_nn.csv'
local_location='~/Wip/dove/p-u/data/Christian_pyqualities_nn.csv'
local_location = path.expanduser(local_location)
if remote_location:
    data_file = remote_location
elif local_location:
    data_file = local_location
else:
    import gtk

    if gtk.pygtk_version < (2,3,90):
	print "PyGtk 2.3.90 or later required for PyQualities"
	raise SystemExit
    dialog = gtk.FileChooserDialog("PyQualities .csv file...",
				   None,
				   gtk.FILE_CHOOSER_ACTION_OPEN,
				   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    dafilter = gtk.FileFilter()
    dafilter.set_name("Text files")
    dafilter.add_mime_type("text/plain")
    dafilter.add_pattern("*.txt")
    dialog.add_filter(dafilter)
    
    dafilter = gtk.FileFilter()
    dafilter.set_name("All files")
    dafilter.add_pattern("*")
    dialog.add_filter(dafilter)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
	data_file = dialog.get_data_file()
	print dialog.get_data_file(), 'selected'
    elif response == gtk.RESPONSE_CANCEL:
	print 'Closed, no files selected'
    dialog.destroy()

full_df = pd.read_csv(data_file)

adjectives_cols = set(full_df.columns) #begin making list of adjective columns
adjectives_cols.remove('name')
adjectives_cols.remove('how well do they know me (by me)')
adjectives_cols.remove('how well do they know me (by them)')
adjectives_cols.remove('sexual relationship') # this is the list of adjective columns
adjectives_cols = list(adjectives_cols)

max_score = full_df.drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1).applymap(lambda x: x+1).count(axis=1)[0]
full_df[adjectives_cols] = full_df[adjectives_cols].applymap(lambda x: max_score - x) # redefining scores based on the computed max_score
full_df[adjectives_cols] = full_df[adjectives_cols].applymap(lambda x: 0 if x == max_score else x)
full_df[adjectives_cols] = full_df[adjectives_cols].applymap(lambda x: x / (max_score-1))



me_df = full_df[full_df['name'] == 'me'].drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1).dropna(axis=1).T
me_df = me_df[me_df != 0.0].dropna(how='all')
me_df = me_df.sort(columns=[0], ascending=False)
full_df = full_df[full_df['name'] != 'me'] # drop the row containingy my ratings

sexual_rel_df = full_df[full_df['sexual relationship'] == True].drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1).T
sexual_rel_res = pd.DataFrame({'means' : sexual_rel_df.mean(axis=1), 'sems' : sem(sexual_rel_df.T)})
sexual_rel_res = sexual_rel_res[sexual_rel_res != 0.0].dropna(how='all') # drop rows containing onyl null values
sexual_rel_res = sexual_rel_res.sort(columns=['means'], ascending=False)

nsexual_rel_df = full_df[full_df['sexual relationship'] != True].drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1).T
nsexual_rel_res = pd.DataFrame({'means' : nsexual_rel_df.mean(axis=1), 'sems' : sem(nsexual_rel_df.T)})
nsexual_rel_res = nsexual_rel_res[nsexual_rel_res != 0.0].dropna(how='all') # drop rows containing onyl null values
nsexual_rel_res = nsexual_rel_res.sort(columns=['means'], ascending=False)

fig = figure(figsize=(8,12),facecolor='#eeeeee',  tight_layout=True)

ids_me = me_df.index
ind_me = np.arange(len(me_df))
width = 0.35
ax1 = fig.add_subplot(311)
ax1.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
ax1.set_xticklabels(ids_me,fontsize=9,rotation=60)
ax1.set_xticks(ind_me + width/2)
ax1.bar(ind_me,me_df[0], width, color='m', alpha=0.4, zorder = 1)
ax1.set_ylabel('My Normalized Ratings', fontsize='11')
axis.Axis.zoom(ax1.xaxis, -0.5)
ax1.set_ylim(0, 1.05)

ids_sex = sexual_rel_res.index
ind_sex = np.arange(len(sexual_rel_res))
width = 0.35
ax2 = fig.add_subplot(312)
ax2.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
ax2.set_xticklabels(ids_sex,fontsize=9,rotation=60)
ax2.set_xticks(ind_sex + width/2)
ax2.bar(ind_sex,sexual_rel_res['means'], width, color='m', alpha=0.4, zorder = 1)
ax2.errorbar(ind_sex+width/2, sexual_rel_res['means'], yerr=sexual_rel_res['sems'], ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
ax2.set_ylabel('Normalized Ratings by \n Sexual Partners', fontsize='11', multialignment='center')
axis.Axis.zoom(ax2.xaxis, -0.5)
ax2.set_ylim(0, 1.05)

ids_nsex = nsexual_rel_res.index
ind_nsex = np.arange(len(nsexual_rel_res))
width = 0.35
ax3 = fig.add_subplot(313)
ax3.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
ax3.set_xticklabels(ids_nsex,fontsize=9,rotation=60)
ax3.set_xticks(ind_nsex + width/2)
ax3.bar(ind_nsex,nsexual_rel_res['means'], width, color='m', alpha=0.4, zorder = 1)
ax3.errorbar(ind_nsex+width/2, nsexual_rel_res['means'], yerr=nsexual_rel_res['sems'], ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
ax3.set_ylabel('Normalized Ratings excluding \n Sexual Partners', fontsize='11', multialignment='center')
axis.Axis.zoom(ax3.xaxis, -0.5)
ax3.set_ylim(0, 1.05)

show()
