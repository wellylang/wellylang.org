# wellylang.org

Sources for the [wellylang.org](http://www.wellylang.org) website.

## Dependencies

To build the website, you will need:

- [Python](https://www.python.org/downloads/) 2.7, or Python 3.3 or later.

- [Foundation 6](https://foundation.zurb.com/sites/download.html/complete)

  Place it in `../foundation` (or edit `make.sh` to configure the path).

- [Nancy](https://github.com/rrthomas/nancy/releases)

  Make sure the "nancy" command is on your path. For example, add the
  following to your `.bashrc` file:
  ```
  $ export PATH=$PATH:/path/to/nancy
  ```
  Nancy requires certain Perl dependencies: File::Slurp and File::Which.
  See the Nancy `README.md` for details.

## Layout

Source files are in `src`. When you run `make.sh`, the website is constructed
in `build`. Files in `build/js/` and `build/css/` are collected from various
sources, including `src/js/` and `src/css/` respectively. The logo graphics
are copied from `logos`, and the Welly tarballs are copied from `releases`.
The HTML files are constructed by Nancy. See `make.sh` for details.

Each *file* `build/path/to/file.html` corresponds to a *directory*
`src/path/to/file/`. The output file is constructed from `src/template.html`,
which `$include`s the file `src/path/to/file/main.html`. See the
`build()` function in `make.sh` for details.

A few other files are `$include`d by `src/template.html`:

- `title.txt` - Placed in the `<title>` element. The root directory contains
  a `title.txt` file whose contents are simply "Welly". This will be used for
  all pages that do not define a more specific `title.txt`.

- `menu.html` - Placed on the left-hand side of the page. This contains the
  HTML for the navigation menu. It in turn includes files from the `menu`
  directory for each submenu. The submenus are blank by default. Each
  subdirectory overrides one of the submenus with a populated version.

The `releases` directory can be populated by running `get-releases.sh`, if you
have an account on the server. Otherwise, it will be empty. It is not
version-controlled.
