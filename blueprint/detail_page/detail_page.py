from flask import Blueprint, render_template
from blueprint.detail_page.exchange import exchange
from blueprint.detail_page.getdata import corona, embassy, vaccine, kr_name, notice, noticeall, embassy, safe

detail_page = Blueprint("detail_page", __name__, url_prefix="/")

# 상세 페이지
@detail_page.route('/country/<ISO_code>', methods=['GET'])
def country(ISO_code):
    exchange_rate = exchange(ISO_code)
    coronadata = corona(ISO_code)
    vaccinedata = vaccine(ISO_code)
    country_kr = kr_name(ISO_code)
    noticedata = notice(ISO_code)
    allnotice = noticeall(ISO_code)
    embassydata = embassy(ISO_code)
    safedata = safe(ISO_code)
    dataset = {
        'name': country_kr, 'exchange': exchange_rate, 'corona': coronadata,
        'vaccine': vaccinedata, 'notice': noticedata, 'allnotice': allnotice,
        'embassy': embassydata, 'safe': safedata
    }
    return render_template('detail.html', data=dataset)