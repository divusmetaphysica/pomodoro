# Simple CLI Pomodoro Timer

A simple Pomodoro Timer with command line interface. The script uses only
Python standard library and developed/tested with Python `>=3.8`

```bash
➜  pomodoro git:(main) ✗ ./pomodoro.py --help
usage: pomodoro.py [-h] [-w WORK] [-s SHORT] [-l LONG] {short,long,work}

Command line Pomodoro timer.

positional arguments:
  {short,long,work}     Period to wait

optional arguments:
  -h, --help            show this help message and exit
  -w WORK, --work WORK  Default 25 min.
  -s SHORT, --short SHORT
                        Default 5 min.
  -l LONG, --long LONG  Default 15 min.
```

## Usage

To start a timer it is enough to call

```bash
python3 pomodoro.py work
```

For easier use I suggest to make it runnable and set a symbolic link to a
location on `PATH`

```bash
chmod +x ./pomodoro.py

ln -s /path/to/pomodoro.py ~/bin/pomodoro
# or
sudo ln -s /path/to/pomodoro.py /usr/bin/pomodoro
# or
sudo ln -s /path/to/pomodoro.py /usr/local/bin/pomodoro

# run then with
pomodoro work
```

## Configuration

You can add an INI formatted config file, the script searches its location and `$HOME` for a
file named `.pomodoro`, `pomodoro.ini` or `pomodoro.cfg` which should have simple format of

```ini
[pomodoro]
short = 5
long = 15
work = 25
```

This custom config can overridden any time with CLI options.