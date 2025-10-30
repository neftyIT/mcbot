"""Custom exceptions for the Minecraft Discord bot."""


class MinecraftBotError(Exception):
    """Base exception for all Minecraft bot errors."""
    pass


class ServerError(MinecraftBotError):
    """Base exception for server-related errors."""
    pass


class ServerNotRunningError(ServerError):
    """Raised when attempting to interact with a stopped server."""
    def __init__(self, message: str = "The server is not running"):
        self.message = message
        super().__init__(self.message)


class ServerAlreadyRunningError(ServerError):
    """Raised when attempting to start an already running server."""
    def __init__(self, message: str = "The server is already running"):
        self.message = message
        super().__init__(self.message)


class ServerStartupError(ServerError):
    """Raised when the server fails to start."""
    def __init__(self, message: str = "Failed to start the server"):
        self.message = message
        super().__init__(self.message)


class RconError(MinecraftBotError):
    """Base exception for RCON-related errors."""
    pass


class RconConnectionError(RconError):
    """Raised when RCON connection fails."""
    def __init__(self, message: str = "Failed to connect to server via RCON"):
        self.message = message
        super().__init__(self.message)


class RconCommandError(RconError):
    """Raised when RCON command execution fails."""
    def __init__(self, command: str, message: str = ""):
        self.command = command
        self.message = message or f"Failed to execute RCON command: {command}"
        super().__init__(self.message)


class NetworkError(MinecraftBotError):
    """Base exception for network-related errors."""
    pass


class ServerUnreachableError(NetworkError):
    """Raised when the server cannot be reached via network."""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.message = f"Server unreachable at {host}:{port}"
        super().__init__(self.message)


class ConfigurationError(MinecraftBotError):
    """Raised when there's a configuration issue."""
    pass


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing."""
    def __init__(self, key: str):
        self.key = key
        self.message = f"Missing required configuration: {key}"
        super().__init__(self.message)


class InvalidConfigError(ConfigurationError):
    """Raised when configuration is invalid."""
    def __init__(self, key: str, reason: str):
        self.key = key
        self.reason = reason
        self.message = f"Invalid configuration for '{key}': {reason}"
        super().__init__(self.message)