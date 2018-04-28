"""Module contains ConfigManager class"""


class ConfigManager():
    """
    Read config file in applications directory.
    Stores configuration in a dictionary \n
    format for config file :<br />
    TOKEN=YOURTOKEN <br />
    LAUNCHCMD=COMMAND TO LAUNCH THE SERVER <br />
    CWD=PATH TO THE SERVER FOLDER <br />
    Place the file named config to the project root folder.
    The launch command must contain path to the server.jar file.
    """

    def __init__(self):
        """Create config, by reading the config file"""
        self.filename = "./config"
        self.conf = {}
        self.createConfig()

    def readFile(self):
        """
        Read file to array of strings\n
        returns: string[]
        """
        file_object = open(self.filename, "r")
        content = file_object.read()
        content = content.split("\n")
        return content

    def createConfig(self):
        """Create dictionary of the configuration"""
        content = self.readFile()
        for line in content:
            if not line == "":
                key, val = line.split("=")
                try:
                    self.conf[key] = val
                except KeyError:
                    print("Check your config file, see further details",
                          " in documentation",
                          " botSrc.configmanager.ConfigManager")
                except ValueError:
                    print("Check your config file, see further details",
                          " in documentation",
                          " botSrc.configmanager.ConfigManager")

    def getToken(self):
        """Return value of token from dictionary"""
        return self.conf["TOKEN"]

    def getWorkPath(self):
        """Return value of work path from dictionary"""
        return self.conf["CWD"]

    def getLaunchCommand(self):
        """Return value of launch commmand from dictionary"""
        return self.conf["LAUNCHCMD"]


if __name__ == '__main__':
    cfgman = ConfigManager()
    print(cfgman.getToken(), cfgman.getLaunchCommand())
