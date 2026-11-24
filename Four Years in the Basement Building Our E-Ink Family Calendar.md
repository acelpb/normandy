# Four Years in the Basement: Building Our E-Ink Family Calendar

Nov 2, 2026 · @Augustin

After four years in a box in my basement, our e-ink family calendar went from "one day" to running on our table in a single Sunday afternoon and an early Monday morning.

Every maker has that box. Mine held a giant e-paper screen, a Raspberry Pi and a battery board, bought with great ambition and then quietly filed under "later". Each time I went down for something else, it looked at me. I looked away.

This weekend my 11-year-old asked what was in it. That was all it took. We opened it, laid everything on the table, and decided to build it together, one step at a time, with an AI assistant (Claude) as our patient guide, speaking French for his benefit. He typed the commands. I mostly held the coffee.

## What was in the box

Three pieces, all of which still worked after four years of patient waiting.

| Part | What it does |
| --- | --- |
| Waveshare 12.48" e-Paper Module (B), 1304 x 984 | The screen: black, white and red. Keeps its image with zero power. |
| Raspberry Pi Zero W (v1.1) | The brain. Tiny, slow, but it has Wi-Fi. |
| PiSugar 3, 1200 mAh | Battery under the Pi, plus a real-time clock that can wake it up. |

&#91;image: The contents of the box: the Waveshare e-paper driver board on its acrylic stand, the PiSugar 3 still in its plastic case, and the Pi Zero W next to a Raspberry Pi 2\]

*Four years of patience, unboxed. The Raspberry Pi 2 came along for the ride but stayed on the bench: no Wi-Fi.*

The screen is really four smaller panels glued together, each with its own chip-select line. Waveshare's driver hides that, mostly. A full refresh takes about 37 seconds according to [Waveshare's own specs](<https://www.waveshare.com/wiki/12.48inch_e-Paper_Module_(B)>), and it blinks dramatically while doing it. My son decided this was a feature.

## Sunday afternoon: from SD card to first pixels

The first hour was pure satisfaction. Raspberry Pi Imager on the Mac, Raspberry Pi OS Lite, Wi-Fi and SSH set in advance, and five minutes later a steady green LED. My son typed `ssh` for the first time and was "inside the Raspberry Pi". He named it `otocal`, which is now its name forever.

Then came the good part: the bugs. Each one was a small detective story.

- **The SPI trap.** We enabled the Pi's SPI interface, as you would for most screens. The test script answered with a wall of `xGpioHandleRequest: Invalid argument`. The answer was in the README my son had opened on his own initiative a few minutes earlier: this driver does SPI "by hand" on the GPIO pins, and the kernel's SPI driver was squatting on them. We switched SPI off again.
- **Ancient Python.** Next error: `module 'time' has no attribute 'clock'`. The demo still calls `time.clock()`, which Python removed years ago. One `sed` replaced it with `time.perf_counter()`.
- **The first image.** No errors, lots of blinking, and about two minutes per image on the little Zero. Straight, complete, and with red in it. We cheered at a slowly blinking rectangle.

## The calendar comes alive

Before writing a line of code, my son drew up the spec: the next four weeks, a zoom on today and tomorrow, birthdays in red, holidays as bars. Weather and a "phrase of the day" were nice-to-haves. We mocked it up, he loved it, and that mock-up became the target.

Our family calendar already lives on our self-hosted Nextcloud, so the Pi reads it over CalDAV with the `caldav` Python library. A few choices kept it simple and safe:

- **An app password**, not the real one, stored in a file only the Pi user can read and kept out of the code folder.
- **Initials instead of colours.** The screen has three colours, not one per person, so each family member's calendar gets a short prefix like `AB ·`.
- **Tiny fixes, not a framework.** Duplicate events (one in a personal calendar, one in the family one) are skipped, anything starting with "Anniversaire" turns red, and all-day events stop showing as "00:00".

The best workflow trick: **draft before printing.** A refresh takes about two minutes, so the drawing code first saves a PNG preview, which we copy to the Mac with `scp` and inspect. Only when the preview looks right does it go to the real screen. The first real render, our actual family weeks in ink, was a genuinely great moment.

## Cutting the cord

The screen holds its image without power, so the Pi does not need to stay awake. The plan: wake up, fetch, draw, refresh, set the next alarm, and power off completely.

- **Finding the PiSugar.** `i2cdetect` showed addresses 57 and 68: the PiSugar and its clock were talking to the Pi.
- **Locking it down.** The PiSugar Power Manager opens a web dashboard and a command port to the whole network by default. We removed the web UI and bound the command port to `127.0.0.1` only.
- **A clock stuck in 2020.** The battery's clock had never been set. One `rtc_pi2rtc` command fixed that, and every cycle now resyncs it.
- **One alarm, three wake-ups.** The clock holds a single alarm, like an old bedside clock. So each run sets the *next* one: 06:00, then 11:30, then 18:00, then 06:00 again.
- **An escape hatch.** A Pi that powers itself off after four minutes is hard to work on. If a file named `RESTER_ALLUME` exists, or the battery is charging, it stays on.

Then the scary test: alarm set five minutes ahead, Pi off, fingers crossed. It woke up on its own, drew the calendar and went back to sleep. A small detail in the logs made us smile: the service "waited" eight minutes between two lines. It hadn't. The Pi Zero has no clock of its own, so it boots with the time it shut down at, then jumps forward when it reads the PiSugar's clock.

## Monday, 5 a.m.: the polish

Yes, we kept going before sunrise the next morning. The calendar picked up the details that make it ours:

- **Weather** from [Open-Meteo](https://open-meteo.com/en/docs), free for non-commercial use and with no API key. Its weather codes become small icons we draw ourselves out of circles, lines and polygons. The sun and the lightning bolt are red, because we can.
- **A joke of the day,** picked at random at every wake-up from a text file my son curates. Fair warning: the 2003 joke e-book we first grabbed turned out to be mostly not family-friendly, so the list is now hand-picked.
- **A battery gauge** in the corner, which turns red below 20%.
- **A red frame on today,** at my son's request.
- **A thicker line between Thursday and Friday,** which he spotted. 1304 pixels divided by 7 days is 186.29, so two rounded borders landed side by side. Computing each edge with the same formula fixed it.
- **Emoji tofu.** An event with an emoji drew an empty box. Now a small whitelist maps a few emoji to black-and-white symbols (⭐ becomes ★) and anything else becomes ⚠.

&#91;image: The calendar preview: today and tomorrow with weather icons, four weeks of family events, today framed in red, a joke and the battery level\]

*The latest preview, taken just before the weather icons and the bolder grid font landed.*

## What I learned, and what's next

The box was never the hard part. Starting was. Four years of "I'll need a free weekend" turned out to be one afternoon and one early morning, mostly because we went one small step at a time and celebrated each one.

- **Let the kid drive.** He typed every command, read error messages out loud, and read the README before anyone told him to. He also found the line bug.
- **Small steps, real feedback.** Every step ended with something visible: a green LED, a list of calendars, a PNG, a blinking screen.
- **Keep the code simple.** No framework, a handful of short Python files, and everything in git on GitHub.
- **Bugs are the fun part.** Each one taught something real: GPIO ownership, Python history, pixel rounding, Unicode.

Next up: measure the battery drain per cycle, check that the PiSugar truly cuts power when the Pi is off, and maybe swap the bit-banged SPI for hardware SPI to shorten each refresh. But honestly? It already works. It's on the table, it wakes itself up three times a day, and it tells us a joke.

Go open your box.
