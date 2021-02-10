import pexpect


def run_script(user, host, port, password, script_path, args=None):
    ssh_command = f'ssh {user}@{host} -p {port} "bash -s" -- < {script_path} {args or ""}'

    child = pexpect.spawn('/bin/bash', ['-c', ssh_command], encoding="utf-8")
    child.expect("(?i)password:")
    child.sendline(password)
    child.expect(pexpect.EOF)

    return child.before
