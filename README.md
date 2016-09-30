# wellylang.org
Sources for the wellylang.org website.

To build the web-site, you will need:

 - Foundation 6, which you can download from here:

    http://foundation.zurb.com/sites/download.html/complete

   Place it in ../foundation-6.2.3-complete (or edit "make.sh" to configure the path).

 - Google Prettifier, which you can download as follows:

    $ git clone https://github.com/google/code-prettify

   Place it in ../code-prettify (or edit "make.sh" to configure the path).

 - Nancy, which you can download from here:

    https://github.com/rrthomas/nancy

   Make sure the "nancy" command is on your path. For example, add the following to your ".bashrc" file:

    export PATH=$PATH:/path/to/nancy

   Nancy requires certain Perl dependencies: File::Slurp and File::Which. See the Nancy README for
   details.
