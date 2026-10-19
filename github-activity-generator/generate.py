#!/usr/bin/env python3
"""Build a clearly labeled synthetic Git activity demonstration locally."""
import argparse
import os
import random
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

START = date(2026, 6, 1)
END = date(2026, 10, 19)
WEIGHTS = [30, 30, 20, 8, 7, 3, 1, 1]


def git(*args, cwd, env=None, capture=False):
    return subprocess.run(['git', *args], cwd=cwd, env=env, check=True,
                          text=True, stdout=subprocess.PIPE if capture else subprocess.DEVNULL).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='synthetic-activity-repo', help='New folder for the Git repository')
    parser.add_argument('--name', help='Commit author name (defaults to git config user.name)')
    parser.add_argument('--email', help='Commit author email (defaults to git config user.email)')
    args = parser.parse_args()
    root = Path(args.output).resolve()
    if root.exists():
        parser.error(f'Output already exists: {root}. Choose another --output to avoid overwriting files.')
    def get_config(key):
        p = subprocess.run(['git', 'config', '--get', key], capture_output=True, text=True)
        return p.stdout.strip() if p.returncode == 0 else ''
    name = args.name or get_config('user.name')
    email = args.email or get_config('user.email')
    if not name or not email:
        parser.error('Provide --name and --email (the email must be associated with your GitHub account).')
    root.mkdir(parents=True)
    git('init', '-b', 'main', cwd=root)
    git('config', 'user.name', name, cwd=root)
    git('config', 'user.email', email, cwd=root)
    (root / 'README.md').write_text('# Synthetic Activity Demonstration\n\nThis repository contains generated, backdated demonstration commits.\nIt is **not** a record of work performed on the corresponding dates.\n')
    (root / 'activity.txt').write_text('Synthetic log (not an actual historical work diary)\n')
    rng = random.Random(42)
    day = START
    count_total = 0
    while day <= END:
        count = rng.choices(range(1, 9), weights=WEIGHTS, k=1)[0]
        # Small variation in time, without changing the calendar date.
        minutes = sorted(rng.sample(range(9 * 60, 21 * 60), count))
        for n, minute_of_day in enumerate(minutes, 1):
            moment = datetime(day.year, day.month, day.day,
                              minute_of_day // 60, minute_of_day % 60,
                              tzinfo=timezone(timedelta(hours=-5)))
            with (root / 'activity.txt').open('a') as f:
                f.write(f'{moment.isoformat()} | synthetic entry {n} of {count}\n')
            git('add', 'activity.txt', 'README.md', cwd=root)
            env = os.environ.copy()
            env['GIT_AUTHOR_DATE'] = moment.isoformat()
            env['GIT_COMMITTER_DATE'] = moment.isoformat()
            git('commit', '-m', f'Synthetic activity entry for {day.isoformat()} ({n}/{count})', cwd=root, env=env)
            count_total += 1
        day += timedelta(days=1)
    print(f'Created {count_total} synthetic commits across {(END - START).days+1} consecutive dates.')
    print(f'Repository: {root}')
    print('Next: create an EMPTY private GitHub repo, then follow the push steps in SETUP.md.')


if __name__ == '__main__':
    main()
