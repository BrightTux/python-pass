Rofi pass replacement for Wayland
--------

I recently updated my system to use wayland on [Aeon](https://en.opensuse.org/Portal:Aeon).
Since it officially only supports wayland (instead of X11) and Gnome, i could not get any of
the [other pass extensions](https://wiki.archlinux.org/title/Pass) to work. I also tried utilizing
[passff](https://github.com/passff/passff) but could not get it working with the flatpak firefox
combined with the distrobox exports and etc.

This extension was birth forth from there as a result.

Dependencies:
* `tree`
* `gpg`
* `xclip`
* `pass`

Installation:
1. create and source a virtual env, and install the required package.
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

1. Update the `shebang` in the pypass.py file

1. Create a keyboard shortcut to launch the script.


