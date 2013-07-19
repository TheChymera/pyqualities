#!/usr/bin/env python
__author__ = 'Horea Christian'
import numpy as np
import matplotlib.dates as mdates
from matplotlib.pyplot import text
import itertools
import pandas as pd
from os import path
from pylab import math, datetime, figure, tick_params, legend, xlabel, ylabel, title, matplotlib, show

remote_location =''
local_location='~/Wip/dove/p-u/data/Christian-pyqualities.csv'
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
max_score = len(full_df.drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1))
me_df = full_df[full_df['name'] == 'me'].drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1).dropna(axis=1).T
#~ me_df = me_df.reindex()
#~ print me_df.set_index(max_score - np.arange(len(me_df)))

sexual_rel_df = full_df[full_df['sexual relationship'] == True].drop(['name','how well do they know me (by me)','how well do they know me (by them)','sexual relationship'], axis=1).T
sexual_rel_df = sexual_rel_df.set_index(max_score - np.arange(len(sexual_rel_df)))
sexual_rel_df['score'] = sexual_rel_df.index
sexual_rel_df = pd.melt(sexual_rel_df, "score").rename(columns={"value": "quals"}).dropna()[["quals", "score"]]
sexual_rel_res = sexual_rel_df.groupby(['quals']).mean()
sexual_rel_res['std'] = ''
sexual_rel_res['std'] = sexual_rel_df.groupby(['quals']).std()
sexual_rel_res = sexual_rel_res.sort(columns=['score'], ascending=False)

ids_sex = sexual_rel_res.index
ind_sex = np.arange(len(sexual_rel_res))
width = 0.35
fig = figure(facecolor='#eeeeee',  tight_layout=True)
ax1 = fig.add_subplot(311)
ax1.set_xticklabels(ids_sex,fontsize=9,rotation=30)
ax1.bar(ind_sex+width,np.array(sexual_rel_res['score']).T, width, color='m', yerr=np.array(sexual_rel_res['std']).T)
text(0.5,0.5, 'lala',fontsize=12)
show()
