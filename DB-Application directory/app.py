from project import app


if __name__ == "__main__":
    app.logger.info('Application Started')
    app.run(debug=True)