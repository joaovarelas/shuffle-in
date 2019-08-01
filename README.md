# shuffle-in
Webapp to shuffle between random musics of different styles.

Using Python Flask 1.1.1 with Jinja2 templates support and several API's.

More than 10 Million of discography available, according to Discogs.

![ShuffleIn](https://i.imgur.com/ZCRoufU.png)


# Install & Run

Generate your API tokens at Discogs and Google (Youtube) and edit them
at `shuffle.py` file.



`$ python -m pip install --user Flask`

`$ git clone https://github.com/joaovarelas/shuffle-in`

`$ cd shuffle-in`

`$ export FLASK_APP=shuffle.py && python -m flask run`


Web server runs on http://127.0.0.1:5000/ by default.
