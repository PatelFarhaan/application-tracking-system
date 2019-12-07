from project import app


if __name__ == "__main__":
    ####################################################################################################################
    import logging

    logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename='/media/farhaan/New Volume/Masters/CMPE226_TEAM1_SOURCES/LOG/app.log',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
    ####################################################################################################################
    app.run(debug=True)