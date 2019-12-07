from project import app


if __name__ == "__main__":
    ####################################################################################################################
    import logging

    logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename=app.config['LOG_PATH'],
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
    ####################################################################################################################
    app.run(debug=True)