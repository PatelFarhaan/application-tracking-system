from flask import render_template, Blueprint, app


error_page_blueprint = Blueprint('error_page', __name__)


@error_page_blueprint.app_errorhandler(404)
def error_404(e):
    app.logger.info('Page Not Found')
    return render_template('error_pages/404.html'), 404


@error_page_blueprint.app_errorhandler(403)
def error_403(e):
    app.logger.info('Forbidden Page')
    return render_template('error_pages/403.html'), 403