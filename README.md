# xblock-pdf

[![Build Status](https://travis-ci.org/open-craft/xblock-pdf.svg?branch=master)](https://travis-ci.org/github/open-craft/xblock-pdf)

> Course component (Open edX XBlock) that provides an easy way to embed a PDF

## Features

- Download button available
- (Optional) Source document download button, for example to provide your PPT file
- Create tracking logs:
  - `edx.pdf.loaded` when a student loads the PDF
  - `edx.pdf.downloaded` when a student downloads the PDF

## Customize the XBlock

By default, PDF Download Allowed is set to `True`.
The default value can  be changed in `xblock-pdf/pdf/ pdf.py`

## Install / Update the XBlock

Add it to the `EDXAPP_EXTRA_REQUIREMENTS` variable.

```yml
EDXAPP_EXTRA_REQUIREMENTS:
  - name: 'git+https://github.com/open-craft/xblock-pdf.git@v1.0.1#egg=xblock-pdf'
```

Then run your deployment playbooks.

### Restart your Open edX processes

```shell
sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
```

# Use the XBlock

### Activate the XBlock in your course

Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["pdf"]`.

### Use the XBlock in a unit

Select `Advanced -> PDF` in your unit.

### Custom Configurations

Below is a table of custom django settings configurations that can be used with the xblock.

| Configuration | Description |
|---- |---- |
| `PDFXBLOCK_DISABLE_ALL_DOWNLOAD` | Disables all downloadables (download pdf/source) in the XBlock if set to `True`. Overrides all custom download pdf options set in Studio, without overwriting them.

## Development environment

For the code quality environment, you need to install both Python and JavaScript requirements.

Run the following:

    npm install -g grunt-cli
    npm install

Then, preferably in a [virtualenv](https://virtualenv.pypa.io), run

    pip install -r requirements.txt


Then, run `grunt test` to assess code quality.

## License

GNU Affero General Public License 3.0 (AGPL 3.0)
