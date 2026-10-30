# Working on this course

Install Quarto >= 1.10.19, then run:

```sh
quarto render
quarto preview
```

Edit `_quarto.yml` to set metadata and navigation. It uses JSON syntax, which is
valid YAML. Add lessons and practice tasks under their respective directories;
keep observable learning objectives and assessment criteria aligned. Add every
student page to the render list or its explicit glob. Use meaningful headings,
figure descriptions and accessible alternatives to required activities.

Instructor notes are excluded from the default render list but remain in the
source repository. Private assessment material needs separate access control.
Inspect the rendered `_site/` contents before distribution. Rendering does not
publish anything. The template code uses the accompanying LICENSE; choose and
document appropriate rights for your own content, figures and data.

Record exact R/Python environments before adding executable examples. The
starter itself has no R/Python runtime dependencies and makes no API calls.
