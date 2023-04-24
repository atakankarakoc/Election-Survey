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
    data = elections.data_scrapt()
    grouped_data = {}
    #We group the data we collect according to the survey companies.
    #Data belonging to the same survey companies are combined.
    grouped_data = grouping(data, grouped_data)
    total_vote = total_vote_calc(grouped_data)

    metropoll_y = []
    asal_y = []
    areda_y = []
    iea_y = []
    saros_y = []
    yoneylem_y = []
    artibir_y = []
    optimar_y = []
    avrasya_y = []
    bulgu_y = []
    orc_y = []
    mak_y = []
    aksoy_y = []
    genar_y = []
    themis_y = []
    piar_y = []

    value_lists = [[] for i in range(len(grouped_data[0]))]
    for d in grouped_data:
        for i, value in enumerate(d.values()):
            value_lists[i].append(value)

    for l, j in zip(value_lists, range(len(value_lists))):
        if (j == 0 or j == 1):
            continue
        else:
            metropoll_y.append(l[0])
            asal_y.append(l[1])
            areda_y.append(l[2])
            iea_y.append(l[3])
            saros_y.append(l[4])
            yoneylem_y.append(l[5])
            artibir_y.append(l[6])
            optimar_y.append(l[7])
            avrasya_y.append(l[8])
            bulgu_y.append(l[9])
            orc_y.append(l[10])
            mak_y.append(l[11])
            aksoy_y.append(l[12])
            genar_y.append(l[13])
            themis_y.append(l[14])
            piar_y.append(l[15])

    grouped_y = [metropoll_y, asal_y, areda_y, iea_y, saros_y, yoneylem_y, artibir_y, optimar_y, avrasya_y,
                 bulgu_y, orc_y, mak_y, aksoy_y, genar_y, themis_y, piar_y]

    #We get an output by redirecting the result of our operations to index.html on the localhost.
    return render_template("index.html",
                           title="Elections Graphics",
                           data=grouped_data,
                           total=total_vote,
                           bar=bar_chart(grouped_y, grouped_data),
                           pie=pie_chart(grouped_y, grouped_data)
                        )


def grouping(data, grouped_data):
    grouped_data_list = []
    """
        Checking whether the data is in the empty list by accessing the company name 
        and then performing the addition operations. 
        If the data has been added before, this time the 2 data is combined.
    """
    for d in data:
        name = d['company']
        if name not in grouped_data:
            grouped_data[name] = {
                'company': d['company'],
                'sample': d['sample'],
                'akp_vote': d['akp_vote'],
                'mhp_vote': d['mhp_vote'],
                'bbp_vote': d['bbp_vote'],
                'yrp_vote': d['yrp_vote'],
                'chp_vote': d['chp_vote'],
                'iyi_vote': d['iyi_vote'],
                'deva_vote': d['deva_vote'],
                'gp_vote': d['gp_vote'],
                'sp_vote': d['sp_vote'],
                'dp_vote': d['dp_vote'],
                'ysgp_vote': d['ysgp_vote'],
                'tip_vote': d['tip_vote'],
                'zp_vote': d['zp_vote'],
                'mp_vote': d['mp_vote'],
                'tdp_vote': d['tdp_vote'],
                'btp_vote': d['btp_vote'],
                'others_vote': d['others_vote']
            }
        else:
            grouped_data[name]['sample'] += d['sample']
            grouped_data[name]['akp_vote'] += d['akp_vote']
            grouped_data[name]['mhp_vote'] += d['mhp_vote']
            grouped_data[name]['bbp_vote'] += d['bbp_vote']
            grouped_data[name]['yrp_vote'] += d['yrp_vote']
            grouped_data[name]['chp_vote'] += d['chp_vote']
            grouped_data[name]['iyi_vote'] += d['iyi_vote']
            grouped_data[name]['deva_vote'] += d['deva_vote']
            grouped_data[name]['gp_vote'] += d['gp_vote']
            grouped_data[name]['sp_vote'] += d['sp_vote']
            grouped_data[name]['dp_vote'] += d['dp_vote']
            grouped_data[name]['ysgp_vote'] += d['ysgp_vote']
            grouped_data[name]['tip_vote'] += d['tip_vote']
            grouped_data[name]['zp_vote'] += d['zp_vote']
            grouped_data[name]['tdp_vote'] += d['tdp_vote']
            grouped_data[name]['btp_vote'] += d['btp_vote']
            grouped_data[name]['others_vote'] += d['others_vote']
    #A new dictionary was created because my keys became company names
    #while my values became all the rest of the data.
    for key, value in grouped_data.items():
        grouped_data_list.append(
            {
                'company': key,
                'sample': value['sample'],
                'akp_vote': value['akp_vote'],
                'mhp_vote': value['mhp_vote'],
                'bbp_vote': value['bbp_vote'],
                'yrp_vote': value['yrp_vote'],
                'chp_vote': value['chp_vote'],
                'iyi_vote': value['iyi_vote'],
                'deva_vote': value['deva_vote'],
                'gp_vote': value['gp_vote'],
                'sp_vote': value['sp_vote'],
                'dp_vote': value['dp_vote'],
                'ysgp_vote': value['ysgp_vote'],
                'tip_vote': value['tip_vote'],
                'zp_vote': value['zp_vote'],
                'mp_vote': value['mp_vote'],
                'tdp_vote': value['tdp_vote'],
                'btp_vote': value['btp_vote'],
                'others_vote': value['others_vote']
            }
        )
    return grouped_data_list

def total_vote_calc(grouped_data):
    company = "-"
    totals = [0] * 19
    for n in grouped_data:
        totals[0] = company
        totals[1] += n['sample']
        totals[2] += n['akp_vote']
        totals[3] += n['mhp_vote']
        totals[4] += n['bbp_vote']
        totals[5] += n['yrp_vote']
        totals[6] += n['chp_vote']
        totals[7] += n['iyi_vote']
        totals[8] += n['deva_vote']
        totals[9] += n['gp_vote']
        totals[10] += n['sp_vote']
        totals[11] += n['dp_vote']
        totals[12] += n['ysgp_vote']
        totals[13] += n['tip_vote']
        totals[14] += n['zp_vote']
        totals[15] += n['mp_vote']
        totals[16] += n['tdp_vote']
        totals[17] += n['btp_vote']
        totals[18] += n['others_vote']

    return totals

def bar_chart(y, data):
    x = ["AKP", "MHP", "BBP", "YRP", "CHP", "İYİ", "DEVA", "GP",
         "SP", "DP", "YSGP", "TİP", "ZP", "MP", "TDP", "BTP", "OTHERS"]
    colors = ['#ff8700', '#c8102e', '#e31e24', '#976114', '#ed1822', '#44b2e3', '#006d9e', '#2db34a',
              '#cf3338', '#fbac8f', '#3a913f', '#b61f23', '#404040', '#1d5fa4', '#f76f92', '#ff4747', '#000000']
    for d in data:
        if d['company'] == 'MetroPOLL':
            fig = plt.figure()
            plt.bar(x, y[0], color=colors)
            plt.xlabel("Parties")
            plt.ylabel("Party Vote Count")
            plt.title("MetroPOLL Company Election Survey Bar Chart")
            plt.xticks(rotation=90)
            plt.yticks(rotation=0,
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
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
                       ticks=[50, 100, 500, 1000, 3000, 7000, 10000],
                       labels=["50", "100", "500", "1000", "3000", "7000", "10000"])
            plt.semilogy()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            piar_bar = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        else:
            print("company is not found")
    return metropoll_bar, asal_bar, areda_bar, iea_bar, saros_bar, yoneylem_bar, artibir_bar, \
        optimar_bar, avrasya_bar,bulgu_bar, orc_bar, mak_bar, aksoy_bar, genar_bar, themis_bar, piar_bar


def pie_chart(y, data):
    x = ["AKP", "MHP", "BBP", "YRP", "CHP", "İYİ", "DEVA", "GP",
         "SP", "DP", "YSGP", "TİP", "ZP", "MP", "TDP", "BTP", "OTHERS"]
    colors = ['#ff8700', '#c8102e', '#e31e24', '#976114', '#ed1822', '#44b2e3', '#006d9e', '#2db34a',
              '#cf3338', '#fbac8f', '#3a913f', '#b61f23', '#404040', '#1d5fa4', '#f76f92', '#ff4747', '#000000']
    for d in data:
        if d['company'] == 'MetroPOLL':
            fig = plt.figure()
            plt.pie(y[0], labels=x, labeldistance=1.2, colors=colors)
            plt.title('MetroPOLL Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            metropoll_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ASAL':
            fig = plt.figure()
            plt.pie(y[1], labels=x, labeldistance=1.2, colors=colors)
            plt.title('ASAL Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            asal_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Areda Survey':
            fig = plt.figure()
            plt.pie(y[2], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Areda Survey Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            areda_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'İEA':
            fig = plt.figure()
            plt.pie(y[3], labels=x, labeldistance=1.2, colors=colors)
            plt.title('İEA Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            iea_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'SAROS':
            fig = plt.figure()
            plt.pie(y[4], labels=x, labeldistance=1.2, colors=colors)
            plt.title('SAROS Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            saros_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Yöneylem':
            fig = plt.figure()
            plt.pie(y[5], labels=x, labeldistance=1.2, colors=colors)
            plt.title('SAROS Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            yoneylem_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Artıbir':
            fig = plt.figure()
            plt.pie(y[6], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Artıbir Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            artibir_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Optimar':
            fig = plt.figure()
            plt.pie(y[7], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Optimar Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            optimar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Avrasya':
            fig = plt.figure()
            plt.pie(y[8], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Avrasya Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            avrasya_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Bulgu':
            fig = plt.figure()
            plt.pie(y[9], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Bulgu Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            bulgu_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'ORC':
            fig = plt.figure()
            plt.pie(y[10], labels=x, labeldistance=1.2, colors=colors)
            plt.title('ORC Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            orc_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'MAK':
            fig = plt.figure()
            plt.pie(y[11], labels=x, labeldistance=1.2, colors=colors)
            plt.title('MAK Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            mak_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Aksoy':
            fig = plt.figure()
            plt.pie(y[12], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Aksoy Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            aksoy_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'GENAR':
            fig = plt.figure()
            plt.pie(y[13], labels=x, labeldistance=1.2, colors=colors)
            plt.title('GENAR Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            genar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Themis':
            fig = plt.figure()
            plt.pie(y[14], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Themis Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            themis_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        elif d['company'] == 'Piar':
            fig = plt.figure()
            plt.pie(y[15], labels=x, labeldistance=1.2, colors=colors)
            plt.title('Piar Company Election Survey Pie Chart')
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            piar_pie = base64.b64encode(img.getvalue()).decode('utf-8')
            plt.close(fig)
        else:
            print("company is not found.")
    return metropoll_pie, asal_pie, areda_pie, iea_pie, saros_pie, yoneylem_pie, artibir_pie, optimar_pie, avrasya_pie, \
        bulgu_pie, orc_pie, mak_pie, aksoy_pie, genar_pie, themis_pie, piar_pie

if __name__ == "__main__":
    app.run(debug=True)