from flask import Blueprint, render_template

error_pages = Blueprint(
    "error_pages",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/error_pages/static/",
)


@error_pages.app_errorhandler(404)
def page_not_found(error):
    return render_template("error_pages/page_not_found.html"), 404


@error_pages.app_errorhandler(500)
def internal_server_error(error):
    return render_template("error_pages/server_error.html"), 500


# add other error handler here