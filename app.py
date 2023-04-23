from flask import Flask
from flask import render_template
from elections import Election

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
    #We get an output by redirecting the result of our operations to index.html on the localhost.
    return render_template("index.html",
                           title="Elections Graphics",
                           data=grouped_data
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


if __name__ == "__main__":
    app.run(debug=True)