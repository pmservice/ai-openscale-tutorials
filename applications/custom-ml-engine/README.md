## PythonWebAppwithFlaskKVVPG

Basic Web project with Python with Flask

[![](https://img.shields.io/badge/IBM%20Cloud-powered-blue.svg)](https://bluemix.net)
![Platform](https://img.shields.io/badge/platform-PYTHON-lightgrey.svg?style=flat)

### Table of Contents
* [Summary](#summary)
* [Requirements](#requirements)
* [Configuration](#configuration)
* [Run](#run)
* [Debug](#debug)

<a name="summary"></a>
### Summary
The Web basic starter contains an opinionated set of files for web serving:

- `public/index.html`
- `public/404.html`
- `public/500.html`



<a name="enablement"></a>
### IBM Cloud Enablement

<a name="requirements"></a>
### Requirements
#### Local Development Tools Setup (optional)

- If you don't already have it, install [Python](https://www.python.org/downloads/)

#### IBM Cloud development tools setup (optional)

1. Install [IBM Cloud Developer Tools](https://console.bluemix.net/docs/cli/idt/setting_up_idt.html#add-cli) on your machine  
2. Install the plugin with: `bx plugin install dev -r bluemix`


#### IBM Cloud DevOps setup (optional)

[![Create Toolchain](https://console.ng.bluemix.net/devops/graphics/create_toolchain_button.png)](https://console.ng.bluemix.net/devops/setup/deploy/)

[IBM Cloud DevOps](https://www.ibm.com/cloud-computing/bluemix/devops) services provides toolchains as a set of tool integrations that support development, deployment, and operations tasks inside IBM Cloud. The "Create Toolchain" button creates a DevOps toolchain and acts as a single-click deploy to IBM Cloud including provisioning all required services. 

***Note** you must publish your project to [Github](https://github.com/) for this to work.



<a name="configuration"></a>
### Configuration

The project contains IBM Cloud specific files that are used to deploy the application as part of an IBM Cloud DevOps flow. The `.bluemix` directory contains files used to define the IBM Cloud toolchain and pipeline for your application. The `manifest.yml` file specifies the name of your application in IBM Cloud, the timeout value during deployment, and which services to bind to.

Credentials are either taken from the VCAP_SERVICES environment variable if in IBM Cloud, or from a config file if running locally. 


<a name="run"></a>
### Run
#### Using IBM Cloud development CLI
The IBM Cloud development plugin makes it easy to compile and run your application if you do not have all of the tools installed on your computer yet. Your application will be compiled with Docker containers. To compile and run your app, run:

```bash
bx dev build
bx dev run
```


#### Using your local development environment


Running flask applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app.

##### Usage
```bash
python manage.py subcommand [ipaddress]
```

##### Subcommands
`manage.py` offers a variety of different run commands to match the proper situation:
* `start`: starts a server in a production setting using `gunicorn`.
* `run`: starts a native flask development server. This includes backend reloading upon file saves and the Werkzeug stack-trace debugger for diagnosing runtime failures in-browser.
* `livereload`: starts a development server via the `livereload` package. This includes backend reloading as well as dynamic frontend browser reloading. The Werkzeug stack-trace debugger will be disabled, so this is only recommended when working on frontend development.
* `debug`: starts a native flask development server, but with the native reloader/tracer disabled. This leaves the debug port exposed to be attached to an IDE (such as PyCharm's `Attach to Local Process`)

There are also a few utility commands:
* `build`: compiles `.py` files within the project directory into `.pyc` files
* `test`: runs all unit tests inside of the project's `test` directory


##### Endpoints

Your application is running at: `http://localhost:3000/` in your browser.

- Health endpoint: `/health`



<a name="debug"></a>
### Debug

#### Using IBM Cloud development CLI
To build and debug your app, run:
```bash
bx dev build --debug
bx dev debug
```
#### Using your local development environment
There are two different options for debugging a `flask` project:
1. Run `python manage.py runserver` to start a native flask development server. This comes with the Werkzeug stack-trace debugger, which will present runtime failure stack-traces in-browser with the ability to inspect objects at any point in the trace. For more information, see [Werkzeug documentation](http://werkzeug.pocoo.org/).
2. Run `python manage.py debug` to run a flask development server with debug exposed, but the native debugger/reloader turned off. This grants access for an IDE to attach itself to the process (i.e. in PyCharm, use `Run` -> `Attach to Local Process`)

