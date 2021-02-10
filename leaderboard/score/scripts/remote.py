import pexpect


async def _run_script_ssh(user, host, password, script_path, port=22, args=None):
    ssh_command = f'ssh {user}@{host} -p {port} -o "StrictHostKeyChecking=no" "bash -s" -- < {script_path} {args or ""}'

    child = pexpect.spawn("/bin/bash", ["-c", ssh_command], encoding="utf-8")

    await child.expect("password:", async_=True)
    child.sendline(password)

    await child.expect(pexpect.EOF, async_=True)

    return child.before


def _get_password(user):
    # Assumes previously configured linode machine running
    # https://github.com/eduardofcgo/gago-node
    return f"{user}2004{user}2005"


def _get_host(user):
    # Assumes correctly configured /etc/hosts file
    return user


def _get_user():
    return "root"


async def run_script(user, script_path):
    return await _run_script_ssh(
        _get_user(), _get_host(user), _get_password(user), script_path
    )
