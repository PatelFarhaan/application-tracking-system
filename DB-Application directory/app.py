from project import app


if __name__ == "__main__":
    ####################################################################################################################
    import logging

    logging.basicConfig(format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        filename='/home/ubuntu/application_tracking_system/LOG/app.log',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        filemode='a')
    ####################################################################################################################
    app.run(host='0.0.0.0', port=80,debug=True)
