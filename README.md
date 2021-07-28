# twitter searcher
example ETL process which searches tweeds using MongoDB and PosgreSQL in docker containers

API &rarr; MongoDB &rarr; ETL &rarr; PostgrSQL &rarr; output

## Installation / Usage

```
* download the files into a separate directory
* cd to this directory
* add your twitter keys in twitter_tweets/config.py
* modify search term in twitter_tweets/get_tweets_streaming.py (last line)
* run "docker-composer up" in terminal
* look at results in evaluation/evaluate.csv
```
