# tinyeducation

## About 

In this repo I will be storing resources to help teach children as I embark on the journey of learning myself to teach my children.


## Games: Toddler learning games

### Game 1: Phonics Keyboard (Alphabet Learning Game)

A simple, engaging Pygame game to help young children (toddlers ~3 years old) learn the alphabet and basic keyboard skills.

The game shows big letters, plays the phonetic sound repeatedly, and gives satisfying visual + audio feedback (green flash + bounce) when the correct key is pressed. It shows total/average time at the end.

#### Quick Start (easiest way)

```bash
# 1. Install dependency (once)
pip install pygame

# 2. Run from the repo root (no need to cd into the game folder)
python3 games/phonics-keyboard/game.py
```

- Starts in a large **windowed** mode by default (auto-sized to nearly fill your screen while staying a normal window).
- Press **SPACE**, **ENTER**, or click **Ready** to begin.
- Press the matching letter key when you see it.
- **ESC** quits anytime.
- Use `-f` / `--fullscreen` if you want the old immersive fullscreen mode.

Examples:

```bash
python3 games/phonics-keyboard/game.py --help          # See all options
python3 games/phonics-keyboard/game.py -f              # Fullscreen
python3 games/phonics-keyboard/game.py --width 1920 --height 1080   # Force exact size
```

All asset paths are resolved relative to the script, so you can run it from anywhere once pygame is installed.

#### Installation notes
- Python 3.10+ recommended.
- The 26 MP3 sound files (`alphasounds-a.mp3` ... `alphasounds-z.mp3`) and `correct.wav` + the font are already included in the repo under `games/phonics-keyboard/`.
- On Linux, if you get audio or fullscreen issues, try the system package instead: `sudo apt install python3-pygame`.

## Credits
- **Alphabet Sounds**: Provided by [Sound City Reading](https://www.soundcityreading.net/individual-alphabet-sounds---abc-order.html). These materials are copyrighted by Kathryn J. Davis, but permission is granted for parents, teachers, and tutors to use them for educational purposes with their students. Thank you to Sound City Reading for making these resources freely available!
- **Font**: [School Yard](https://www.dafont.com/school-yard.font) dafont
