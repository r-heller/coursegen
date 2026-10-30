# coursegen

A reusable Quarto course template with a syllabus, measurable learning outcomes,
lessons, practice, a feedback rubric, and instructor notes excluded from the
default student website.

Requires Python >= 3.9 and [Quarto](https://quarto.org/docs/get-started/) >= 1.10.19.

```sh
python3 scripts/new_project.py ../my-course --title "My Course" --author "R. Heller"
cd ../my-course
quarto render
quarto preview
```

Use `--language de` or `--language fr` for interface labels; translate the actual
content separately. The destination must not exist. The result is standalone
and does not depend on this repository. See `template/README.md` for editing,
licensing and distribution.

The sample is a 30-minute lesson on recording a synthetic calculation. It is a
template demonstration, not an accredited course. Instructor-source files are
not private merely because they are excluded from rendering: store confidential
assessment material separately and inspect distributed artifacts.

Run `python3 -m unittest discover -s tests -v` for scaffold checks. CI creates
and renders a fresh course and checks that instructor notes are absent from
the student artifact. Publication remains a separate action.

Local acceptance evidence and remaining scope: [MAINTENANCE.md](MAINTENANCE.md).
