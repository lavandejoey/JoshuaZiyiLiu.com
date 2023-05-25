#!/usr/bin/env python
# apis/ip.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
from flask import blueprints, request, current_app, make_response, jsonify, redirect
from flask_babel import refresh

ip_blueprint = blueprints.Blueprint(name="ip", import_name=__name__, static_folder="static", static_url_path="/static",
                                    template_folder="templates", url_prefix="/", subdomain=None, url_defaults=None,
                                    cli_group=None)


def get_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ipa_addr = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ipa_addr = request.remote_addr
    return ipa_addr


def get_timezone():
    return request.headers.get("Time-Zone")


def get_locale():
    cookie = request.cookies.get('locale')
    print(cookie)
    if cookie in current_app.config.get('LANGUAGES'):
        return cookie
    return request.accept_languages.best_match(current_app.config.get('BABEL_DEFAULT_LOCALE'))
    # 没有cookie时，默认为 en


@ip_blueprint.route('/set-locale/<language>')
def set_locale(language):
    resp = redirect(request.referrer)
    if language:
        resp.set_cookie('locale', language, max_age=30 * 24 * 60 * 60)
    return resp

#
# @ip_blueprint.route("/lang", methods=['POST'])
# def set_locale():
#     lang = request.args.get("language")
#     response = make_response(jsonify(message=lang))
#     if lang == 'English':
#         refresh()
#         response.set_cookie('locale', 'en')
#         return response
#
#     if lang == '汉语':
#         refresh()
#         response.set_cookie('locale', 'zh_CN')
#         return response
#
#     return jsonify({"data": "success"})