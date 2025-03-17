import datetime
import shlex
import subprocess

BLOCKLIST = {
    "rm", "mv", "cp", "chmod", "chown", "dd", "kill", "reboot", "shutdown", "systemctl", "service",
    "mkfs", "mount", "umount", "passwd", "iptables", "ufw", "adduser", "deluser", "wget", "curl",
}


def subprocess_run_command(command: str) -> str:
    """Run a command in a subprocess.

    Note:
        Do not run commands that will change the system state.
        This function blocks the following commands that modify system state,
        such as `rm`, `mv`, `chmod`, etc.

    Examples:
        >>> subprocess_run_command("pwd")
        /Users/user/Documents

    Args:
        command: Complete command to run, as it would be entered in the terminal

    Returns:
        str: The text that is printed to stdout
    """

    print(f"Running {command}")

    args = shlex.split(command)

    if not args:
        return "Error: No command provided."

    if args[0] in BLOCKLIST:
        return f"Error: Command '{args[0]}' is not allowed."
    elif args[0].lower() == "echo" and any(arg in BLOCKLIST for arg in args[1:]):
        return f"Error: Command '{args[0]}' is not allowed."
    try:
        res = subprocess.run(args, capture_output=True, text=True, timeout=5).stdout
    except Exception as e:
        print(f"Error: {e}")
        return str(e)
    print(res)
    return res



def get_current_date_time() -> str:
    """Get the current local date and time in ISO 8601 format.

    Examples:
        >>> get_current_date_time()
        2025-03-16T10:30:45.123456-04:00

    Returns:
        str: The current local date and time in an ISO 8601 formatted string.
    """

    timestamp = datetime.datetime.now().astimezone().strftime("%I:%M:%S %p %Z on %A %B %d, %Y")
    output = f"It is currently {timestamp}"
    return output
