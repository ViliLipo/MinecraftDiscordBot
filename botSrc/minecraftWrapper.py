#! /usr/bin/python3
import subprocess
import asyncio
import sys
import select


class MinecraftWrapper:
    """
    MinecraftWrapper enables asynchronously running I/O to
    minecraftserver that is runned as a subprocess.
    """

    def __init__(self):
        print("init")
        self.runningMc = "not born yet"
        self.serverIsOn = False

    async def execute(self, cmd, workdir):
        """
        Executes given command in given workpath asynchronously.
        Yiels continuosly output as a string\n
        - :param cmd: Complete bash shell command string\n
        - :param workdir: Working directory for command\n
        - :type cmd: string\n
        - :type workdir: string\n
        """
        if self.serverIsOn:
            return
        process = await asyncio.create_subprocess_shell(
                                                        cmd,
                                                        cwd=workdir,
                                                        stdout=asyncio.subprocess.PIPE,
                                                        stdin=asyncio.subprocess.PIPE)
        while(process.returncode is None):
            self.serverIsOn = True
            data = await process.stdout.readline()
            self.runningMc = process
            # print(self.runningMc)
            line = data.decode().strip()
            if(line != ""):
                yield line
            await asyncio.sleep(0)
        return_code = process.wait()
        self.serverIsOn = False
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    async def say(self, name, message):
        """
        Passes "say" command to minecraftserver with given message
        and inserts the senders username to the message\n

        - :param name: Name of the sender\n
        - :param message: Message to be sent\n
        - :type name: string \n
        - :type message: string\n
        """
        line = '/say <{0:1}>{1:1}\n'.format(name, message)
        print(line)
        print(self.runningMc)
        self.runningMc.stdin.write(line.encode('utf-8'))
        #  self.runnigMc.stdin.flush()
        await asyncio.sleep(0)

    async def serverCommand(self, name, command):
        """
        Passses command given in parameters straight to the minecraftserver.
        ATTENTION the server naturally has OP-level access to the commandline.
        if "say" command is used the MinecraftWrapper.say(self, name ,message)
        method is used to insert Username to message\n

        - :param name: Username of the command issuer \n
        - :param command: Command to be issued \n
        """
        if "say" in command:
            command = command.replace('say', '', 1)
            await self.say(name, command)
            return
        line = command + '\n'
        self.runningMc.stdin.write(line.encode('utf-8'))
        await asyncio.sleep(0)

    def isAValidMessage(self, line):
            """
            Checks given line for expressions that are not for public\n
            - :param line: Line to be checked\n
            - :type line: string\n
            - :returns: boolean
            """
            value = True
            if ("[User Authenticator" in line
                    or "logged in with entity id" in line):
                value = False
            if "[Server thread/WARN]:" in line:
                value = False
            return value

    def formatLine(self, line):
        """
        Cuts unwanted parts from given line. \n
        - :param line: Line to be formatted \n
        - :type line: string \n
        - :returns string: \n
        """
        line = line.split("] ", 1)[1]
        line = line.replace("[Server]", '', 1)
        line = line.replace('[Server thread/INFO]:', '', 1)
        line = line.strip()
        return line

    async def minecraft(self):
        """
        Minecraft uses MinecraftWrapper.execute(self, cmd, workdir) and yields
        server console output strings in a formatted form, also
        prints the unformatted form to console
        """
        cmd = "java -Xmx1024M -Xms1024M -jar" +  \
            " /home/vili/Applications/Minecraft/server/server.jar nogui"
        cwd = "/home/vili/Applications/Minecraft/server/"
        async for line in self.execute(cmd, cwd):
            print(line)  # the raw unformatted data is for the host
            if self.isAValidMessage(line):
                line = self.formatLine(line)
                if not line == "":
                    yield line

    async def cliInput(self):
        """
        Asynchronously polls  sys.stdin and passes the input lines to the
        minecraft-server-subprocess stdin.
        """
        while True:
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line:
                    self.runningMc.stdin.write(line.encode('utf-8'))
                    await asyncio.sleep(0.1)
                else:
                    print('eof')
            else:
                await asyncio.sleep(0.1)

    async def cliOutput(self):
            """
            Runs MinecraftWrapper.minecraft(self) and prints its output to
            the terminal asynchronously
            """
            async for line in self.minecraft():
                print(line)
                await asyncio.sleep(0)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    mc = MinecraftWrapper()
    try:
        tasks = [loop.create_task(mc.cliOutput()),
                 loop.create_task(mc.cliInput())]
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()
