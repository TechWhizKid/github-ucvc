# GitHub - User Content Version Checker

**A Python module that allows you to check for new releases of any app on GitHub by reading a version file from its repository.**

## Get Started

- To use **`github-ucvc`**, you can either clone the project using **Git**:

```bash
git clone --depth 1 https://github.com/TechWhizKid/github-ucvc.git
```

- Or simply click **[here](https://github.com/TechWhizKid/github-ucvc/blob/main/github_ucvc.py)** to download the main file “**github_ucvc.py**”

## Usage

This project allows you to compare versions of your software in three different ways: by release date, by release type, and by release version. You need to create a **`*.ini`** file with a section for version info and upload it to your GitHub repository. Then, you can use the methods from the **`compare_version`** class to compare your current version with the latest release.

- To compare by release date, use the format **`dd-mm-yyyy`** for the date and the **`compare_by_rdate()`** method. For example:

```ini
[version_info]
latest_release_date=03-03-2024
```

```py
from github_ucvc import compare_version as cv

# cv(current_version, version_file_url, section, key, debug)
checker = cv("03-03-2024", "https://raw.githubusercontent.com/TechWhizKid/github-ucvc/main/version.ini",
                              "version_info", "latest_release_date", debug=True)

if checker.compare_by_rdate() == 0:
    print("\nINFO: You have the latest version.")
elif checker.compare_by_rdate() == 1:
    print("\nINFO: A newer version is available.")
```

- To compare by release type, use one of the following values: alpha`1`, preview`2`, beta`3`, or release`4` for the type and the **`compare_by_rtype()`** method. For example:

```ini
[version_info]
latest_release_type=preview
```

```py
from github_ucvc import compare_version as cv

# cv(current_version, version_file_url, section, key, debug)
checker = cv("alpha", "https://raw.githubusercontent.com/TechWhizKid/github-ucvc/main/version.ini",
                              "version_info", "latest_release_type", debug=True)

if checker.compare_by_rtype() == 0:
    print("\nINFO: You have the latest version.")
elif checker.compare_by_rtype() == 1:
    print("\nINFO: A newer version is available.")
```

- To compare by release version, use the format `MAJOR`**.**`MINOR`**.**`PATCH` for the version and the **`compare_by_version()`** method. For example:

```ini
[version_info]
latest_release_version=1.2.2
```

```py
from github_ucvc import compare_version as cv

# cv(current_version, version_file_url, section, key, debug)
checker = cv("1.2.2", "https://raw.githubusercontent.com/TechWhizKid/github-ucvc/main/version.ini",
                              "version_info", "latest_release_type", debug=True)

if checker.compare_by_version() == 0:
    print("\nINFO: You have the latest version.")
elif checker.compare_by_version() == 1:
    print("\nINFO: A newer version is available.")
```

- If your version file is not in **`*.ini`** format, you can use the **`get_version_files_text()`** method to get the file’s text and process it manually. For example:

```py
from github_ucvc import compare_version as cv

version_file_url = "https://raw.githubusercontent.com/TechWhizKid/github-ucvc/main/version.ini"
content = cv().get_version_files_text(version_file_url)

print(content) # You can now use the text to compare versions manually
```

**NOTE:** You can set the debug argument to false (debug=False) if you don’t want the code to exit on any error such as, invalid data in version file or invalid url.

### All the return values

```log
0: The current version is up to date.
1: The current version is older than the latest release.
2: Invalid file URL provided or network error.
3: Version file does not contain the section name specified.
4: Invalid date format provided.
5: Invalid version format provided.
6: Invalid current version type provided.
7: Invalid latest version type provided.
```

# How to contribute

This project is open to contributions and feedback from anyone who is interested in improving it. If you have any ideas for other ways to compare versions or other features that you would like to see, please feel free to share them. You can do so by creating an issue or a pull request on the GitHub repository. I appreciate your input and support. 😊
