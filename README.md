# E444-F2026-PRA3

Author: Ali Alyaseri

This repository is a clone of <https://github.com/miguelgrinberg/flasky>. I am using it to complete the Flask and Docker activities for ECE444 PRA3.

## Local summary

For Activity 1.2, I reproduced examples 2-1 and 2-2 from the Flask textbook. Example 2-1 adds a basic home page that displays `Hello World!`. Example 2-2 adds a dynamic route that displays the name included in the URL.

## How to run the examples

From the root of this repository, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Flask and the extensions used by the examples:

```bash
python -m pip install Flask Flask-Bootstrap Flask-Moment
```

Start the development server:

```bash
flask --app hello run --debug
```

Open these pages in a browser:

- Example 2-1: <http://127.0.0.1:5000/>
- Example 2-2: <http://127.0.0.1:5000/user/Ali>

The name at the end of the second URL can be changed to test the dynamic route. For example, `/user/Sam` displays `Hello, Sam!`.

Press `Control-C` in the terminal to stop the server. Run `deactivate` when the virtual environment is no longer needed.

## Activity 1.3

For Activity 1.3, I moved the page into Jinja templates and added a Bootstrap navigation bar. The home page displays my name and uses Flask-Moment to show the local date and time in `LLLL` format.

![Activity 1.3 webpage with a navigation bar, personalized heading, and timestamp](screenshots/activity-1-3.png)
