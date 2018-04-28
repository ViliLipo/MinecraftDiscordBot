<h1 id="botSrc">botSrc</h1>


<h1 id="botSrc.minecraftWrapper">botSrc.minecraftWrapper</h1>


<h2 id="botSrc.minecraftWrapper.MinecraftWrapper">MinecraftWrapper</h2>

```python
MinecraftWrapper(self)
```

MinecraftWrapper enables asynchronously running I/O to
minecraftserver that is runned as a subprocess.

<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.execute">execute</h3>

```python
MinecraftWrapper.execute(self, cmd, workdir)
```

Executes given command in given workpath asynchronously.
Yields continuosly output as a string

- :param cmd: Complete bash shell command string

- :param workdir: Working directory for command

- :type cmd: string

- :type workdir: string


<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.say">say</h3>

```python
MinecraftWrapper.say(self, name, message)
```

Passes "say" command to minecraftserver with given message
and inserts the senders username to the message


- :param name: Name of the sender

- :param message: Message to be sent

- :type name: string

- :type message: string


<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.serverCommand">serverCommand</h3>

```python
MinecraftWrapper.serverCommand(self, name, command)
```

Passses command given in parameters straight to the minecraftserver.
ATTENTION the server naturally has OP-level access to the commandline.
if "say" command is used the MinecraftWrapper.say(self, name ,message)
method is used to insert Username to message


- :param name: Username of the command issuer

- :param command: Command to be issued


<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.isAValidMessage">isAValidMessage</h3>

```python
MinecraftWrapper.isAValidMessage(self, line)
```

Checks given line for expressions that are not for public

- :param line: Line to be checked

- :type line: string

- :returns: boolean

<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.formatLine">formatLine</h3>

```python
MinecraftWrapper.formatLine(self, line)
```

Cuts unwanted parts from given line.

- :param line: Line to be formatted

- :type line: string

- :returns string:


<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.minecraft">minecraft</h3>

```python
MinecraftWrapper.minecraft(self)
```

Minecraft uses MinecraftWrapper.execute(self, cmd, workdir) and yields
server console output strings in a formatted form, also
prints the unformatted form to console

<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.cliInput">cliInput</h3>

```python
MinecraftWrapper.cliInput(self)
```

Asynchronously polls  sys.stdin and passes the input lines to the
minecraft-server-subprocess stdin.

<h3 id="botSrc.minecraftWrapper.MinecraftWrapper.cliOutput">cliOutput</h3>

```python
MinecraftWrapper.cliOutput(self)
```

Runs MinecraftWrapper.minecraft(self) and prints its output to
the terminal asynchronously

<h1 id="botSrc.bot">botSrc.bot</h1>


<h2 id="botSrc.bot.on_ready">on_ready</h2>

```python
on_ready()
```

When the client has connected, starts minecraftserver and adds
its input and output to asyncio eventloop

<h2 id="botSrc.bot.on_message">on_message</h2>

```python
on_message(message)
```

Messages from regular users are passed as /say commands and messages
from administrators are passed as server commands

<h2 id="botSrc.bot.minecraftFunction">minecraftFunction</h2>

```python
minecraftFunction()
```

Finds channel called minecraft and starts to feed server output
there.

