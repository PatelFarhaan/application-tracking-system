from project import app
from flask import render_template, Blueprint


########################################################################################################################
import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename=app.config['LOG_PATH'],
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
########################################################################################################################

error_page_blueprint = Blueprint('error_page', __name__)


@error_page_blueprint.app_errorhandler(404)
def error_404(e):
    logging.info('Page Not Found')
    return render_template('error_pages/404.html'), 404


@error_page_blueprint.app_errorhandler(403)
def error_403(e):
    logging.info('Forbidden Page')
    return render_template('error_pages/403.html'), 403
