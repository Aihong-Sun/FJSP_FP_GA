import matplotlib.pyplot as plt

color_choice = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite','navy', 'sandybrown', 'moccasin']

plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def Fuzzy_Gantt(JS):
    for i in range(len(JS.Machines)):
        plt.hlines(i,xmin=0,xmax=JS.C_end[2]+5,colors="black")
        ST=JS.Machines[i].start
        for j in range(len(ST)):
            y=[i,i-0.3,i]
            plt.fill_between(ST[j],y,[i,i,i],
                             color=color_choice[JS.Machines[i]._on[j][0]+1]
                             )
            plt.text(x=ST[j][0],y=i-0.4,s='O'+str(JS.Machines[i]._on[j][0]+1)+str(JS.Machines[i]._on[j][1]),size=9)
            plt.text(x=ST[j][0], y=i - 0.1, s=ST[j],size=9)
        ET=JS.Machines[i].end
        for j in range(len(ET)):
            y=[i,i+0.3,i]
            plt.fill_between(ET[j],y,[i,i,i],
                             color=color_choice[JS.Machines[i]._on[j][0]+1]
                             )
            plt.text(x=ET[j][0],y=i+0.4,s='O'+str(JS.Machines[i]._on[j][0]+1)+str(JS.Machines[i]._on[j][1]),size=9)
            plt.text(x=ET[j][0], y=i + 0.1, s=ET[j],size=9)
    plt.yticks([_ for _ in range(i+1)],[_+1 for _ in range(i+1)])
    plt.ylabel('Machines')
    plt.show()


def Gantt_FJSP(JS):
    for i in range(len(JS.Machines)):
        ST=JS.Machines[i].start
        ET=JS.Machines[i].end
        for j in range(len(ST)):
            plt.barh(i , width=ET[j]-ST[j],
                     height=0.8, left=ST[j],
                     color=JS.Machines[i]._on[j][0],
                     edgecolor='black')
            plt.text(x=ST[j],
                     y=i,
                     s=JS.Machines[i]._on,
                     fontsize=12)
    plt.show()


def Gantt_FP(JS):
    y=[]
    y_label=[]
    for i in range(len(JS.Machines)):
        ST=JS.Machines[i].start
        ET=JS.Machines[i].end
        LT=JS.Machines[i].Feed_T
        TT=JS.Machines[i].Tranfer_T
        for j in range(len(ST)):
            plt.barh(i , width=ET[j]-ST[j],
                     height=0.2, left=ST[j],
                     color=color_choice[JS.Machines[i]._on[j][0]],
                     edgecolor='black')
            plt.text(x=ST[j],
                     y=i,
                     s=JS.Machines[i]._on[j][0]+1,
                     fontsize=10)
        y.append(i)
        y_label.append('m'+str(i+1))
        hight=i+0.15
        for m in range(len(TT)):
            plt.barh(hight, width=TT[m][1]-TT[m][0],
                     height=0.1, left=TT[m][0],
                     color='white',
                     edgecolor='black')
        hight+= 0.1
        y.append(hight-0.1)
        y_label.append('travel')
        for k in range(len(LT)):
            for ki in range(len(LT[k])):
                plt.barh(hight, width=LT[k][ki][1]-LT[k][ki][0],
                         height=0.1, left=LT[k][ki][0],
                         color=color_choice[JS.Machines[i].FP_on[k][ki][0]],
                         edgecolor='black')
            hight += 0.1
            y.append(hight-0.1)
            y_label.append('Feedport'+str(k+1))
    plt.yticks(y,y_label)
    plt.show()

def Gantt_FP_box(JS):
    y=[]
    y_label=[]
    for i in range(len(JS.Machines)):
        ST=JS.Machines[i].start
        ET=JS.Machines[i].end
        LT=JS.Machines[i].Feed_T
        TT=JS.Machines[i].Tranfer_T
        for j in range(len(ST)):
            plt.barh(i , width=ET[j]-ST[j],
                     height=0.2, left=ST[j],
                     color=color_choice[JS.Machines[i]._on[j][0]],
                     edgecolor='black')
            plt.text(x=ST[j],
                     y=i,
                     s='J'+str(JS.Machines[i]._on[j][0]+1)+'_B'+str(JS.Machines[i].BT[j]+1),
                     fontsize=6)
        WT=JS.Machines[i].Wait_time
        for Wi in range(len(WT)):
            plt.barh(i, width=WT[Wi][1] - WT[Wi][0],
                     height=0.1, left=WT[Wi][0],
                     color='yellow',
                     zorder=0)
        y.append(i)
        y_label.append('m'+str(i+1))
        hight=i+0.15
        for m in range(len(TT)):
            plt.barh(hight, width=TT[m][1]-TT[m][0],
                     height=0.1, left=TT[m][0],
                     color='white',
                     edgecolor='black')
        hight+= 0.1
        y.append(hight-0.1)
        y_label.append('travel')
        for k in range(len(LT)):
            for ki in range(len(LT[k])):
                plt.barh(hight, width=LT[k][ki][1]-LT[k][ki][0],
                         height=0.1, left=LT[k][ki][0],
                         color=color_choice[JS.Machines[i].FP_on[k][ki][0]],
                         edgecolor='black')
            hight += 0.1
            y.append(hight-0.1)
            y_label.append('Feedport'+str(k+1))
    plt.yticks(y,y_label)
    plt.show()