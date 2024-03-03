import logging
import requests
import configparser


class compare_version:
    def __init__(self, current_version, version_file_url, section, key, debug=False):
        self.current_version = current_version
        self.version_file_url = version_file_url
        self.section = section
        self.key = key
        self.debug = debug

    def get_version_files_text(self, version_file_url):
        try:
            response = requests.get(version_file_url)
            response.raise_for_status()
            content = response.text
        except requests.exceptions.HTTPError as e:
            if self.debug:
                logging.exception(str(e))
            return str("ERROR: Invalid file URL provided or network error.")
        return content

    def compare_by_rdate(self):
        content = self.get_version_files_text(self.version_file_url)
        try:
            config = configparser.ConfigParser()
            config.read_string(content)
            date = config[self.section][self.key]
        except (KeyError, configparser.Error) as e:
            if self.debug:
                logging.exception(str(e))
            return str("ERROR: Version file does not contain 'version_by_date' section.")
        try:
            current_version = int(self.current_version.replace("-", ""))
            date = int(date.replace("-", ""))
        except (Exception, ValueError) as e:
            if self.debug:
                logging.error(str(e))
                return
            return str("ERROR: Invalid date format provided, Correct format is 'dd-mm-yyyy'.")

        if date > current_version:
            return 1
        else:
            return 0
