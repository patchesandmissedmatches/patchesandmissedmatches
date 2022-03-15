import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_pie(slices, plt):
    labels= ['MO', 'ED', 'SP', 'AF', 'DF']
    
    colors = ['r', 'y', 'g', 'b', 'c']

    plt.pie(slices, labels = labels, colors=colors, 
            startangle=90, shadow = True, explode = (0, 0, 0, 0, 0),
            radius = 1, autopct = '%1.1f%%')

    plt.legend()

def create_bar(height, plt):
    left = [1, 2, 3, 4, 5]

    x_label = ['MO', 'ED', 'SP', 'AF', 'DF']

    plt.bar(left, height, tick_label = x_label,
            width = 0.8, color = ['red', 'yellow', 'green', 'blue', 'cyan'])

    plt.xlabel('Classifications', fontsize=20)
    plt.ylabel('Frequency', fontsize=20)
    
def grouped_bar_chart(y0, y1, y2, y3, y4,y5, repo_nr):
    x = np.arange(0, 110, 10)
    width = 0.15
    
    w0 = np.arange(len(y0))
    w1 = [x + width for x in w0]
    w2 = [x + width for x in w1]
    w3 = [x + width for x in w2]
    w4 = [x + width for x in w3]
    w5 = [x + width for x in w4]
    
    plt.figure(figsize=(15,10), dpi=80)
    
    patch1 = mpatches.Patch(color="#e41a1c", label='Missed Opportunity')
    patch2 = mpatches.Patch(color="#377eb8", label='Effort Duplication')
    patch3 = mpatches.Patch(color="#4daf4a", label='Split(MO/ED)')
    patch4 = mpatches.Patch(color='#F5D9E7', label='Added File')
    patch5 = mpatches.Patch(color='#7FC0D0', label='Deleted File')
    patch6 = mpatches.Patch(color='#a65628', label='Uninteresting')
    plt.legend(fontsize=18, loc="upper left", handles = [patch1, patch2, patch3, patch4, patch5, patch6])

    plt.bar(w0, y0, color='#e41a1c', width=width, edgecolor='white', label='Missed Opportunity')
    plt.bar(w1, y1, color='#377eb8', width=width, edgecolor='white', label='Effort Duplication')
    plt.bar(w2, y2, color='#4daf4a', width=width, edgecolor='white', label='Split(MO/ED)')
    plt.bar(w3, y3, color='#F5D9E7', width=width, edgecolor='white', label='Added File')
    plt.bar(w4, y4, color='#7FC0D0', width=width, edgecolor='white', label='Deleted File')
    plt.bar(w5, y5, color='#a65628', width=width, edgecolor='white', label='Uninteresting')

    plt.xlabel('Classifications', fontsize=20)
    plt.ylabel('Frequency', fontsize=20)
    plt.xticks(fontsize = 14)   
    plt.yticks(fontsize = 14) 
    plt.xticks([r + width for r in range(len(y0))], 
               ['0-100', '10-100', '20-100', '30-100', '40-100', '50-100', '60-100', '70-100', '80-100', '90-100'])
    plt.savefig("Plots/Grouped_bar_"+str(repo_nr)+".png", format="PNG", dpi=80, bbox_inches='tight')
    plt.show()
    
def create_all_bars(data, repo_nr):
    fig = plt.figure(figsize=(20,10))
    count = 1
    for i in data:    
        plt.subplot(2, 5, count)
        plt.title("Bar Chart for interval " + i, fontsize=20)
        create_bar(data[i], plt)
        count += 1
            
    plt.savefig("Plots/All_Bars_"+str(repo_nr)+".png", format="PNG")
    plt.show()
        
def create_all_pie(data, repo_nr):
    fig = plt.figure(figsize=(20,10))
    count = 1
    for i in data:    
        plt.subplot(2, 5, count)
        plt.title("Pie Chart for interval " + i, fontsize=20)
        create_pie(data[i], plt)
        count += 1
    plt.savefig("Plots/"+str(repo_nr)+"_All_Pies.png", format="PNG")
    plt.show()
    
def all_class_bar(height, pr_nr, mainline, variant, plotting=False):
    """
        Bar Chart
    """
    left = [1, 2, 3, 4, 5, 6, 7]
    x_label = ['MO', 'ED', 'Split(MO/ED)', 'CC', 'NE', 'NA', 'ERROR']


    plt.figure(figsize=(15,10), dpi=80)
    plt.bar(left, height, tick_label = x_label, width = 0.8, color = ["#e41a1c","#377eb8","#4daf4a","#984ea3", "#ff7f00", "#ffff33", "#a65628"])

    patch1 = mpatches.Patch(color='#e41a1c', label='Missed Opportunity')
    patch2 = mpatches.Patch(color='#377eb8', label='Effort Duplication')
    patch3 = mpatches.Patch(color='#4daf4a', label='Split(MO/ED)')
    patch4 = mpatches.Patch(color='#984ea3', label='Cannot Classify')
    patch5 = mpatches.Patch(color='#ff7f00', label='Not Existing Files')
    patch6 = mpatches.Patch(color='#ffff33', label='Not Applicable')
    patch7 = mpatches.Patch(color='#a65628', label='Error')
   
    plt.legend(fontsize=18, loc="upper left" ,handles = [patch1, patch2, patch3, patch4, patch5, patch6, patch7])
    
    plt.xlabel('Classifications', fontsize=20)
    plt.xticks(fontsize = 14)   
    plt.yticks(fontsize = 14) 
    
    plt.ylabel('Frequency', fontsize=20)
#     plt.savefig("Plots/"+str(pr_nr) + "_All_classes_bar"+".png", format="PNG",  dpi=80, bbox_inches='tight')
    if plotting:
        plt.show()
    
def all_class_bar_w_even_d(height, pr_nr, mainline, variant):
    """
        Bar Chart
    """
    left = [1, 2, 3, 4, 5, 6, 7, 8]
    x_label = ['MO', 'ED', 'SPlit(MO/ED)', 'CC', 'NE', 'NA','EVEN_D', 'ERROR']

    plt.figure(figsize=(15,10), dpi=80)
    plt.bar(left, height, tick_label = x_label, width = 0.8, color = ["#e41a1c","#377eb8","#4daf4a","#984ea3", "#ff7f00", "#ffff33","#FF1493", "#a65628"])

    patch1 = mpatches.Patch(color='#e41a1c', label='Missed Opportunity')
    patch2 = mpatches.Patch(color='#377eb8', label='Effort Duplication')
    patch3 = mpatches.Patch(color='#4daf4a', label='Split(MO/ED)')
    patch4 = mpatches.Patch(color='#984ea3', label='Cannot Classify')
    patch5 = mpatches.Patch(color='#ff7f00', label='Not Existing Files')
    patch6 = mpatches.Patch(color='#ffff33', label='Not Applicable')
    patch7 = mpatches.Patch(color='#FF1493', label='Even Distribution')
    patch8 = mpatches.Patch(color='#a65628', label='Error')
   
    plt.legend(fontsize=18, loc="upper left" ,handles = [patch1, patch2, patch3, patch4, patch5, patch6, patch7, patch8])
    
    plt.xlabel('Classifications', fontsize=20)
    plt.xticks(fontsize = 14)   
    plt.yticks(fontsize = 14) 
    
    plt.ylabel('Frequency', fontsize=20)
    plt.savefig("Plots/All_Classes_Bar_70_EVED_"+str(pr_nr)+".png", format="PNG",  dpi=80, bbox_inches='tight')
    
    if plot:
        plt.show()
    
def all_class_pie(slices, pr_nr, mainline, variant, plotting = False):
    """
        Pie Chart
    """
    x_label = ['Missed Opportunity', 'Effort Duplication', 'Split', 'Cannot Classify', 'Not Existing Files', 'Not Applicable', 'Error']
    colors = ["#e41a1c","#377eb8","#4daf4a","#984ea3", "#ff7f00", "#ffff33", "#a65628"]

    plt.pie(slices, labels = x_label, colors=colors, 
            startangle=0, shadow = True, explode = (0, 0, 0, 0, 0, 0, 0),
            radius = 3, autopct = '%1.1f%%')
    plt.rc('font', size=18)
    plt.rc('legend', fontsize=14)

    plt.legend(loc='center left', bbox_to_anchor=(2,1.5))
    plt.savefig("Plots/"+str(pr_nr)+"_All_classes_pie.png", format="PNG", dpi=80, bbox_inches='tight')
    if plotting:
        plt.show()