import base64
import io
from flask import Flask
from flask import render_template
from elections import Election
import matplotlib.pyplot as plt

"""
    A __name__ argument is passed in the Flask class to create its instance, 
    which is then used to run the application
"""
app = Flask(__name__)
"""
    If we visit the URL we specified in our link, it allows the output of our 
    actions to be displayed on the browser screen opened on the localhost.
"""

@app.route('/')
def index():
    elections = Election(
        link="https://tr.wikipedia.org/wiki/%C3%9Clke_%C3%A7ap%C4%B1nda_2023_T%C3%BCrkiye_genel_"
                "se%C3%A7imleri_i%C3%A7in_yap%C4%B1lan_anketler",
        headless=False
    )
    data, data2 = elections.data_scrapt()
    #We group the data we collect according to the survey companies.
    #Data belonging to the same survey companies are combined.
    grouped_data = grouping(data)
    grouped_data2 = grouping(data2)

    #Sum the votes of each party regardless of the company
    total_vote, total_vote2 = total_vote_calc(grouped_data, grouped_data2)

    #Receiving only the number of votes of the parties according to the company name
    grouped_y, grouped_y2 = grouped_yy(grouped_data, grouped_data2)

    #We get an output by redirecting the result of our operations to index.html on the localhost.
    return render_template("index.html",
                           title="Elections Graphics",
                           data=grouped_data,
                           total=total_vote,
                           table1_bar=bar_chart(grouped_y, grouped_data),
                           table1_pie=pie_chart(grouped_y, grouped_data),
                           data2=grouped_data2,
                           total2=total_vote2,
                           table2_bar=bar_chart2(grouped_y2, grouped_data2),
                           table2_pie=pie_chart2(grouped_y2, grouped_data2),
                        )


def grouping(data):
    #Creating grouped_data with dictionary comprehension
    grouped_data = {
        d['company']: {
            key: sum([x[key] for x in data if x['company'] == d['company']])
            for key in d.keys() if key != 'company'
        }
        for d in data
    }

    #Creating a grouped_data_list
    grouped_data_list = [{'company': key, **value} for key, value in grouped_data.items()]

    return grouped_data_list


def total_vote_calc(grouped_data, grouped_data2):
    company = "-"
    totals = [0] * 15
    totals2 = [0] * 19
    for dict in grouped_data:
        for i, col_name in enumerate(dict):
            if i == 0:
                totals[i] = company
            else:
                totals[i] += dict[col_name]

    for dict in grouped_data2:
        for i, col_name in enumerate(dict):
            if i == 0:
                totals2[i] = company
            else:
                totals2[i] += dict[col_name]

    return totals, totals2

def grouped_yy(grouped_data, grouped_data2):
    metropoll_y, asal_y, areda_y, iea_y, saros_y, yoneylem_y, artibir_y = [], [], [], [], [], [], []
    optimar_y, avrasya_y, bulgu_y, orc_y, mak_y, aksoy_y, genar_y = [], [], [], [], [], [], []
    themis_y, piar_y, area_y, sonar_y, hbs_y, alf_y, artibir_y2 = [], [], [], [], [], [], []
    orc_y2, areda_y2, yoneylem_y2, mak_y2, avrasya_y2, optimar_y2, aksoy_y2 = [], [], [], [], [], [], []
    team_y, tusiar_y, bulgu_y2, area_y2, sonar_y, ada_y, sosyo_y = [], [], [], [], [], [], []

    value_lists = [[] for i in range(len(grouped_data[0]))]
    for d in grouped_data:
        for i, value in enumerate(d.values()):
            value_lists[i].append(value)
    for l, j in zip(value_lists, range(len(value_lists))):
        if (j == 0 or j == 1):
            continue
        else:
            ada_y.append(l[0])
            aksoy_y.append(l[1])
            optimar_y.append(l[2])
            sosyo_y.append(l[3])
            areda_y.append(l[4])
            team_y.append(l[5])
            tusiar_y.append(l[6])
            artibir_y.append(l[7])
            bulgu_y.append(l[8])
            orc_y.append(l[9])
            area_y.append(l[10])
            sonar_y.append(l[11])
            yoneylem_y.append(l[12])
            mak_y.append(l[13])
            hbs_y.append(l[14])
            alf_y.append(l[15])
            avrasya_y.append(l[16])

    grouped_y = [ada_y, aksoy_y, optimar_y, sosyo_y, areda_y, team_y, tusiar_y, artibir_y, bulgu_y,
                 orc_y, area_y, sonar_y, yoneylem_y, mak_y, hbs_y, alf_y, avrasya_y ]

    value_lists = [[] for i in range(len(grouped_data2[0]))]
    for d in grouped_data2:
        for i, value in enumerate(d.values()):
            value_lists[i].append(value)


    for l, j in zip(value_lists, range(len(value_lists))):
        if (j == 0 or j == 1):
            continue
        else:
            metropoll_y.append(l[0])
            asal_y.append(l[1])
            areda_y2.append(l[2])
            iea_y.append(l[3])
            saros_y.append(l[4])
            yoneylem_y2.append(l[5])
            artibir_y2.append(l[6])
            optimar_y2.append(l[7])
            avrasya_y2.append(l[8])
            bulgu_y2.append(l[9])
            orc_y2.append(l[10])
            mak_y2.append(l[11])
            aksoy_y2.append(l[12])
            genar_y.append(l[13])
            themis_y.append(l[14])
            piar_y.append(l[15])

    grouped_y2 = [metropoll_y, asal_y, areda_y2, iea_y, saros_y, yoneylem_y2, artibir_y2, optimar_y2,
                  avrasya_y2, bulgu_y2, orc_y2, mak_y2, aksoy_y2, genar_y, themis_y, piar_y]

    return grouped_y, grouped_y2

#table1 Bar Chart
def bar_chart(y, data):
    x = ["AKP", "MHP", "BBP", "YRP", "CHP", "İYİ", "YSGP", "TİP", "ZP", "MP", "OTHERS"]
    colors = ['#ff8700', '#c8102e', '#e31e24', '#976114', '#ed1822', '#44b2e3', '#3a913f',
              '#b61f23', '#404040', '#1d5fa4', '#9347ff']
    for d in data:
        if d['company'] == 'ADA':
            fig = plt.figure()
            plt.bar(x, y[0], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("ADA Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[0]):
                plt.text(i, v+1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            ada_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Aksoy':
            fig = plt.figure()
            plt.bar(x, y[1], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Aksoy Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[1]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            aksoy_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Optimar':
            fig = plt.figure()
            plt.bar(x, y[2], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Optimar Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[1]):
                plt.text(i, v+1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            optimar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Sosyo Politik':
            fig = plt.figure()
            plt.bar(x, y[3], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Sosyo Politik Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[3]):
                plt.text(i, v+1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            sosyo_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Areda Survey':
            fig = plt.figure()
            plt.bar(x, y[4], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Areda Survey Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[4]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            areda_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'TEAM':
            fig = plt.figure()
            plt.bar(x, y[5], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("TEAM Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[5]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            team_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'TÜSİAR':
            fig = plt.figure()
            plt.bar(x, y[6], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("TÜSİAR Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[6]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            tusiar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Artıbir':
            fig = plt.figure()
            plt.bar(x, y[7], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Artıbir Company Election Survey Bar Chart")
            plt.xticks(rotation=45)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[7]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            artibir_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Bulgu':
            fig = plt.figure()
            plt.bar(x, y[8], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Bulgu Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[8]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            bulgu_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ORC':
            fig = plt.figure()
            plt.bar(x, y[9], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("ORC Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[9]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            orc_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Area':
            fig = plt.figure()
            plt.bar(x, y[10], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Area Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[10]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            area_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'SONAR':
            fig = plt.figure()
            plt.bar(x, y[11], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("SONAR Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[11]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            sonar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Yöneylem':
            fig = plt.figure()
            plt.bar(x, y[12], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Yöneylem Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[12]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            yoneylem_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'MAK':
            fig = plt.figure()
            plt.bar(x, y[13], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("MAK Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=1)
            for i, v in enumerate(y[13]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            mak_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'HBS':
            fig = plt.figure()
            plt.bar(x, y[14], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("HBS Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[12-4]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            hbs_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ALF':
            fig = plt.figure()
            plt.bar(x, y[15], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("ALF Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[15]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            alf_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Avrasya':
            fig = plt.figure()
            plt.bar(x, y[16], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Avrasya Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500],
                       fontsize=12)
            for i, v in enumerate(y[16]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            avrasya_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        else:
            print("company is not found")
    return ada_bar, aksoy_bar, optimar_bar, sosyo_bar, areda_bar, team_bar, tusiar_bar, artibir_bar, \
        bulgu_bar, orc_bar, area_bar, sonar_bar, yoneylem_bar, mak_bar, hbs_bar, alf_bar, avrasya_bar

#Table2 Bar Chart
def bar_chart2(y, data):
    x = ["AKP", "MHP", "BBP", "YRP", "CHP", "İYİ", "DEVA", "GP",
         "SP", "DP", "YSGP", "TİP", "ZP", "MP", "TDP", "BTP", "OTHERS"]
    colors = ['#ff8700', '#c8102e', '#e31e24', '#976114', '#ed1822', '#44b2e3', '#006d9e', '#2db34a',
              '#cf3338', '#fbac8f', '#3a913f', '#b61f23', '#404040', '#1d5fa4', '#f76f92', '#ff4747', '#9347ff']
    for d in data:
        if d['company'] == 'MetroPOLL':
            fig = plt.figure()
            plt.bar(x, y[0], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("MetroPOLL Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[0]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            metropoll_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ASAL':
            fig = plt.figure()
            plt.bar(x, y[1], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("ASAL Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[1]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            asal_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Areda Survey':
            fig = plt.figure()
            plt.bar(x, y[2], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Areda Survey Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[2]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            areda_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'İEA':
            fig = plt.figure()
            plt.bar(x, y[3], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("İEA Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[3]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            iea_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'SAROS':
            fig = plt.figure()
            plt.bar(x, y[4], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("SAROS Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[4]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            saros_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Yöneylem':
            fig = plt.figure()
            plt.bar(x, y[5], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Yöneylem Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[5]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            yoneylem_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Artıbir':
            fig = plt.figure()
            plt.bar(x, y[6], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Artıbir Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[6]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            artibir_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Optimar':
            fig = plt.figure()
            plt.bar(x, y[7], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Optimar Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[7]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            optimar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Avrasya':
            fig = plt.figure()
            plt.bar(x, y[8], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Avrasya Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[8]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            avrasya_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Bulgu':
            fig = plt.figure()
            plt.bar(x, y[9], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Bulgu Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[9]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            bulgu_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ORC':
            fig = plt.figure()
            plt.bar(x, y[10], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("ORC Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[10]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            orc_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'MAK':
            fig = plt.figure()
            plt.bar(x, y[11], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("MAK Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[11]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            mak_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Aksoy':
            fig = plt.figure()
            plt.bar(x, y[12], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Aksoy Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[12]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            aksoy_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'GENAR':
            fig = plt.figure()
            plt.bar(x, y[13], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("GENAR Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[13]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            genar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Themis':
            fig = plt.figure()
            plt.bar(x, y[14], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Themis Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[14]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            themis_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Piar':
            fig = plt.figure()
            plt.bar(x, y[15], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("Piar Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                       labels=[10, 50, 100, 150, 250, 350, 450, 650, 750, 900, 1500, 2000,
                               2500, 4000, 5000, 7000, 8000],
                       fontsize=12)
            for i, v in enumerate(y[15]):
                plt.text(i, v + 1, str(v), ha='center')
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            piar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        else:
            print("company is not found")
    return metropoll_bar, asal_bar, areda_bar, iea_bar, saros_bar, yoneylem_bar, artibir_bar, \
        optimar_bar, avrasya_bar, bulgu_bar, orc_bar, mak_bar, aksoy_bar, genar_bar, themis_bar, piar_bar

#Table1 Pie Chart
def pie_chart(y, data):
    x = ["AKP", "MHP", "BBP", "YRP", "CHP", "İYİ", "YSGP", "TİP", "ZP", "MP", "OTHERS"]
    colors = ['#ff8700', '#c8102e', '#e31e24', '#976114', '#ed1822', '#44b2e3', '#3a913f',
              '#b61f23', '#404040', '#1d5fa4', '#9347ff']
    threshold = 1.5
    def autopct_more_than_threshold(pct):
        return ('%1.1f%%' % pct) if pct >= threshold else ''

    for d in data:
        if d['company'] == 'ADA':
            fig = plt.figure()
            plt.pie(y[0], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('ADA Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            ada_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Aksoy':
            fig = plt.figure()
            plt.pie(y[1], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Aksoy Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            aksoy_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Optimar':
            fig = plt.figure()
            plt.pie(y[3], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Optimar Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            optimar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Sosyo Politik':
            fig = plt.figure()
            plt.pie(y[3], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Sosyo Politik Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            sosyo_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Areda Survey':
            fig = plt.figure()
            plt.pie(y[4], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Areda Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            areda_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'TEAM':
            fig = plt.figure()
            plt.pie(y[5], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('TEAM Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            team_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'TÜSİAR':
            fig = plt.figure()
            plt.pie(y[6], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('TÜSİAR Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            tusiar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Artıbir':
            fig = plt.figure()
            plt.pie(y[7], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Artıbir Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            artibir_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Bulgu':
            fig = plt.figure()
            plt.pie(y[8], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Bulgu Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            bulgu_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ORC':
            fig = plt.figure()
            plt.pie(y[9], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('ORC Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            orc_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Area':
            fig = plt.figure()
            plt.pie(y[10], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Area Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            area_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'SONAR':
            fig = plt.figure()
            plt.pie(y[11], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('SONAR Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            sonar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Yöneylem':
            fig = plt.figure()
            plt.pie(y[12], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Yöneylem Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            yoneylem_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'MAK':
            fig = plt.figure()
            plt.pie(y[13], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('MAK Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            mak_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'HBS':
            fig = plt.figure()
            plt.pie(y[14], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('HBS Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            hbs_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ALF':
            fig = plt.figure()
            plt.pie(y[15], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('ALF Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            alf_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Avrasya':
            fig = plt.figure()
            plt.pie(y[16], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Avrasya Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            avrasya_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)

        else:
            print("company is not found")
    return ada_pie, aksoy_pie, optimar_pie, sosyo_pie, areda_pie, team_pie, tusiar_pie, artibir_pie,\
        bulgu_pie, orc_pie, area_pie, sonar_pie, yoneylem_pie, mak_pie, hbs_pie, alf_pie, avrasya_pie

#Table2 Pie Chart
def pie_chart2(y, data):
    x = ["AKP", "MHP", "BBP", "YRP", "CHP", "İYİ", "DEVA", "GP",
         "SP", "DP", "YSGP", "TİP", "ZP", "MP", "TDP", "BTP", "OTHERS"]
    colors = ['#ff8700', '#c8102e', '#e31e24', '#976114', '#ed1822', '#44b2e3', '#006d9e', '#2db34a',
              '#cf3338', '#fbac8f', '#3a913f', '#b61f23', '#404040', '#1d5fa4', '#f76f92', '#ff4747', '#9347ff']
    threshold = 1.5
    def autopct_more_than_threshold(pct):
        return ('%1.1f%%' % pct) if pct >= threshold else ''

    for d in data:
        if d['company'] == 'MetroPOLL':
            fig = plt.figure()
            plt.pie(y[0], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('MetroPOLL Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            metropoll_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ASAL':
            fig = plt.figure()
            plt.pie(y[1], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('ASAL Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            asal_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Areda Survey':
            fig = plt.figure()
            plt.pie(y[2], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Areda Survey Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            areda_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'İEA':
            fig = plt.figure()
            plt.pie(y[3], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('İEA Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            iea_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'SAROS':
            fig = plt.figure()
            plt.pie(y[4], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('SAROS Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            saros_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Yöneylem':
            fig = plt.figure()
            plt.pie(y[5], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('SAROS Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            yoneylem_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Artıbir':
            fig = plt.figure()
            plt.pie(y[6], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Artıbir Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            artibir_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Optimar':
            fig = plt.figure()
            plt.pie(y[7], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Optimar Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            optimar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Avrasya':
            fig = plt.figure()
            plt.pie(y[8], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Avrasya Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            avrasya_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Bulgu':
            fig = plt.figure()
            plt.pie(y[9], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Bulgu Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            bulgu_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ORC':
            fig = plt.figure()
            plt.pie(y[10], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('ORC Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            orc_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'MAK':
            fig = plt.figure()
            plt.pie(y[11], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('MAK Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            mak_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Aksoy':
            fig = plt.figure()
            plt.pie(y[12], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Aksoy Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            aksoy_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'GENAR':
            fig = plt.figure()
            plt.pie(y[13], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('GENAR Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            genar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Themis':
            fig = plt.figure()
            plt.pie(y[14], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Themis Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            themis_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Piar':
            fig = plt.figure()
            plt.pie(y[15], labels=x, labeldistance=1.2, colors=colors, autopct=autopct_more_than_threshold)
            plt.title('Piar Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            piar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        else:
            print("company is not found.")
    return metropoll_pie, asal_pie, areda_pie, iea_pie, saros_pie, yoneylem_pie, artibir_pie,\
        optimar_pie, avrasya_pie, bulgu_pie, orc_pie, mak_pie, aksoy_pie, genar_pie, themis_pie, piar_pie

if __name__ == "__main__":
    app.run(debug=True)