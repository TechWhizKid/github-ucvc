import logging      # Module to handle HTTP requests
import requests     # Module to handle logging exceptions
import configparser # Module to handle *.ini file


class compare_version:
    """A class that compares the current version of a software with the latest release date from a version file.

    Attributes:
        current_version (str): The current version of the software in "dd-mm-yyyy", "MAJOR.MINOR.PATCH" or release type format.
        version_file_url (str): The URL of the version file that contains the release date, version or release type information.
        section (str): The section name in the version file that contains the release date, version or release type info key.
        key (str): The key name in the version file that contains the release date, version or release type info value.
        debug (bool): A flag that indicates whether to print debug messages or not. Default is False.
    """

    def __init__(self, current_version=None, version_file_url=None, section=None, key=None, debug=False):
        """The constructor of the compare_version class.

        Args:
            current_version (str): The current version of the software in "dd-mm-yyyy", "MAJOR.MINOR.PATCH" or release type format.
            version_file_url (str): The URL of the version file that contains the release date, version or release type information.
            section (str): The section name in the version file that contains the release date, version or release type info key.
            key (str): The key name in the version file that contains the release date, version or release type info value.
            debug (bool): A flag that indicates whether to print debug messages or not. Default is False.
        """
        # Assign the arguments to the instance attributes
        self.current_version = current_version
        self.version_file_url = version_file_url
        self.section = section
        self.key = key
        self.debug = debug

    def get_version_files_text(self, version_file_url):
        """A method that retrieves the text content of the version file from the given URL.

        Args:
            version_file_url (str): The URL of the version file that contains the release date information.

        Returns:
            str: The text content of the version file if successful, or an integer code indicating the error otherwise.
            Possible error codes are:
                2: Invalid file URL provided or network error.
        """
        try:                                          # Try to send a GET request to the version file URL
            response = requests.get(version_file_url)
            response.raise_for_status()               # Check if the response status code is 200 (OK)
            content = response.text                   # Get the text content of the response
        except requests.exceptions.HTTPError as e:    # Handle the HTTPError exception if the status code is not 200
            if self.debug:                            # If debug mode is on, print the error message and the exception details
                print("ERROR: Invalid file URL provided or network error.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.exception(str(e))
            return int(2)                             # Return the error code 2
        return content                                # Return the text content of the version file

    def compare_by_rdate(self):
        """A method that compares the current version of the software with the latest release date from the version file.

        Returns:
            int: A code indicating the result of the comparison.
            Possible codes are:
                0: The current version is up to date.
                1: The current version is older than the latest release date.
                3: Version file does not contain the section name specified.
                4: Invalid date format provided.
        """
        content = self.get_version_files_text(self.version_file_url) # Get the text content of the version file from the URL
        try:                                                         # Try to parse the content as a config file
            config = configparser.ConfigParser()                     # Create a ConfigParser object
            config.read_string(content)                              # Read the content as a string
            rdate = config[self.section][self.key]                   # Get the release date value from the section and key
        # Handle the KeyError or configparser.Error exception if the section or key is not found
        except (KeyError, configparser.Error) as e:
            if self.debug:                                           # If debug mode is on, print the error message and the exception details
                print(f"ERROR: Version file does not contain '{self.section}' section.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.exception(str(e))
            return int(3)                                                # Return the error code 3
        try:                                                             # Try to convert the current version and the release date to integers
            current_version = int(self.current_version.replace("-", "")) # Remove the dashes from the current version and convert to integer
            rdate = int(rdate.replace("-", ""))                          # Remove the dashes from the release date and convert to integer
        except (Exception, ValueError) as e:                             # Handle the Exception or ValueError exception if the conversion fails
            if self.debug:                                               # If debug mode is on, print the error message and the exception details
                print("ERROR: Invalid date format provided.")
                print("Correct format is 'dd-mm-yyyy'.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.error(str(e))
                return
            return int(4)                                                # Return the error code 4

        if rdate > current_version:                                      # Compare the current version and the release date
            return 1                                                     # If the release date is greater than the current version, return 1
        else:
            return 0                                                     # Otherwise, return 0

    def compare_by_version(self):
        """A method that compares the current version of the software with the latest version number from the version file.

        Returns:
            int: A code indicating the result of the comparison.
            Possible codes are:
                0: The current version is equal to or greater than the latest version number.
                1: The current version is less than the latest version number.
                3: Version file does not contain the section name specified.
                5: Invalid version format provided.
        """
        content = self.get_version_files_text(self.version_file_url)  # Get the text content of the version file from the URL
        try:                                                          # Try to parse the content as a config file
            config = configparser.ConfigParser()                      # Create a ConfigParser object
            config.read_string(content)                               # Read the content as a string
            version = config[self.section][self.key]                  # Get the version number value from the section and key
        # Handle the KeyError or configparser.Error exception if the section or key is not found
        except (KeyError, configparser.Error) as e:                   # If debug mode is on, print the error message and the exception details
            if self.debug:
                print(f"ERROR: Version file does not contain '{self.section}' section.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.exception(str(e))
            return int(3)                                                # Return the error code 3
        try:                                                             # Try to convert the current version and the version number to integers
            current_version = int(self.current_version.replace(".", "")) # Remove the dots from the current version and convert to integer
            version = int(version.replace(".", ""))                      # Remove the dots from the version number and convert to integer
        except (Exception, ValueError) as e:                             # Handle the Exception or ValueError exception if the conversion fails
            if self.debug:                                               # If debug mode is on, print the error message and the exception details
                print("ERROR: Invalid version format provided.")
                print("Correct format is 'MAJOR.MINOR.PATCH'.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.error(str(e))
                return
            return int(5)                                                # Return the error code 5

        if version > current_version:                                    # Compare the current version and the version number
            return 1                                                     # If the version number is greater than the current version, return 1
        else:
            return 0                                                     # Otherwise, return 0

    def compare_by_rtype(self):
        """A method that compares the current version of the software with the latest release type from the version file.

        Returns:
            int: A code indicating the result of the comparison.
            Possible codes are:
                0: The current version is equal to or higher than the latest release type.
                1: The current version is lower than the latest release type.
                3: Version file does not contain the section name specified.
                6: Invalid current version type provided.
                7: Invalid latest version type provided.
        """
        content = self.get_version_files_text(self.version_file_url) # Get the text content of the version file from the URL
        try:                                                         # Try to parse the content as a config file
            config = configparser.ConfigParser()                     # Create a ConfigParser object
            config.read_string(content)                              # Read the content as a string
            rtype = config[self.section][self.key]                   # Get the release type value from the section and key
        # Handle the KeyError or configparser.Error exception if the section or key is not found
        except (KeyError, configparser.Error) as e:
            if self.debug:                                           # If debug mode is on, print the error message and the exception details
                print(f"ERROR: Version file does not contain '{self.section}' section.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.exception(str(e))
            # Return the error code 3
            return int(3)
        try: # Try to convert the current version and the release type to integers
            # Assign a numerical value to each release type
            # alpha = 1, preview = 2, beta = 3, release = 4
            if self.current_version == "alpha":
                current_version = 1
            elif self.current_version == "preview":
                current_version = 2
            elif self.current_version == "beta":
                current_version = 3
            elif self.current_version == "release":
                current_version = 4
            else:
                return int(6) # If the current version is not one of the valid types, return the error code 6

            # Assign a numerical value to each release type
            # alpha = 1, preview = 2, beta = 3, release = 4
            if rtype == "alpha":
                rtype = 1
            elif rtype == "preview":
                rtype = 2
            elif rtype == "beta":
                rtype = 3
            elif rtype == "release":
                rtype = 4
            else:
                return int(7) # If the latest version is not one of the valid types, return the error code 7
        # Handle the Exception or ValueError exception if the conversion fails
        except (Exception, ValueError) as e:
            if self.debug:    # If debug mode is on, print the error message and the exception details
                print("ERROR: Invalid release type provided.")
                print("Correct types are 'alpha', 'preview', 'beta' and 'release'.")
                print("\n:: ====== :: ERROR INFO :: ====== ::\n")
                logging.error(str(e))
                return
            return 2          # Return the error code 2

        if rtype > current_version: # Compare the current version and the release type
            return 1                # If the release type is greater than the current version, return 1
        else:
            return 0                # Otherwise, return 0


# Usage example:
if __name__ == "__main__":
    checker = compare_version("03-03-2024", "https://raw.githubusercontent.com/TechWhizKid/github-ucvc/main/version.ini",
                              "version_info", "latest_release_date", debug=True)
    if checker.compare_by_rdate() == 0:
        print(f"\n{checker.compare_by_rdate()} - INFO: Current version is the latest version.")
    elif checker.compare_by_rdate() == 1:
        print(f"\n{checker.compare_by_rdate()} - INFO: There is a newer version out there.")
