#!/usr/bin/python3

import os
import logging
from flask import Flask, request, render_template
import core.core as core
import core.helper as helper
import core.settings as settings


allowed_extension = set(['crx', 'zip', 'xpi', 'tar', 'gzip'])
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension

app = Flask('ExtAnalysis - Browser Extension Analysis Toolkit')
app.config['UPLOAD_FOLDER'] = core.lab_path
app.secret_key = str(os.urandom(24))

@app.errorhandler(404)
def page_not_found(e):
    error_txt = 'The page you are trying to browse does not exist... Please click on the logo to go back to homepage.'
    return render_template('error.html', error_title="Error 404 - Page Not Found!",
                           error_head="The page you are looking for is kinda imaginary!", error_txt=error_txt), 404


@app.errorhandler(500)
def internal_error(e):
    error_txt = 'Welp! There\'s no good way of telling this but something has gone terribly wrong with the program!'
    return render_template('error.html', error_title="Error 500 - Internal Server Error!",
                           error_head="Something seriously went wrong... ", error_txt=error_txt), 500


@app.route("/")
def home():
    core.updatelog('Accessed Main page')
    lic = open(helper.fixpath(core.path + '/LICENSE'), 'r')
    license_text = lic.read()
    cred = open(helper.fixpath(core.path + '/CREDITS'), 'r')
    credits_text = cred.read()
    sett = open(core.settings_file, 'r')
    settings_json = sett.read()
    return render_template("index.html",
                           report_dir=core.reports_path,
                           lab_dir=core.lab_path,
                           license_text=license_text,
                           credits_text=credits_text,
                           virustotal_api=core.virustotal_api,
                           settings_json=settings_json
                           )

# http://127.0.0.1:13337/api?extid=echcggldkblhodogklpincgchnpgcdco&savedir=b
# body: from-data key: query value: dlanalysis
@app.route("/api/", methods=["POST"])
def api():
    if request.method == 'POST':
        # query = request.args.get('query')
        query = request.form['query']
        import frontend.api as processapi
        return (processapi.view(query, request.args))
        # analysis_id = str(processapi.view(query, request.form))
        # return (analysis_id)
    
    
# required to work
@app.route("/log/")
def updatelogs():
    return (core.log)

# http://127.0.0.1:13337/analysis/EXA2023264053423
@app.route('/analysis/<analysis_id>', methods=['GET'])
def show_analysis(analysis_id):
    import frontend.viewresult as viewResult
    return (viewResult.view(analysis_id)), 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    core.print_logo()
    settings.init_settings()

    host = "0.0.0.0"
    port = 13337
    main_url = 'http://{0}:{1}'.format(host, port)
    # webbrowser.open(main_url)
    print('\n[~] Starting ExtAnalysis at: {0} \n\n'.format(main_url))
    app.run(host=host, port=port)

    # app.run()
