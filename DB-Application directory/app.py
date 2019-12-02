from project import app
import logging, logging.config, yaml

if __name__ == "__main__":
    logging.config.dictConfig(yaml.load(open('logging.conf')))
    logfile = logging.getLogger('file')
    logconsole = logging.getLogger('console')
    logfile.debug("Debug FILE")
    logconsole.debug("Debug CONSOLE")
    app.run(debug=True)