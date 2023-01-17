# Flask-Forum
Forum created in flask

## Features

1. Register users
2. Login users
3. reset password (currently only with outlook)
4. Create new posts
5. Edit posts
6. Show outside post info
7. Show inside post info
8. Do real-time 'like' or 'dislike' to post 
9. Do real-time comment to post 
10. Edit comment
11. Navigation pages
12. Option to choose how many posts per page
13. Marking tag when hover on that tag
14. Filter posts by name
15. Filter posts by tag
16. RSS feed for new posts

## Pre-requestment
### Virtual enviroment
1. Make a new directory, for example: ```path/to/my_project```
2. Make a virtual enviroment and activate it

### Installing Libraries

Install ```Flask``` library:

```pip install Flask```

Install ```bleach``` library:

```pip install bleach```

Install ```Markdown``` library:

```pip install Markdown```

Install ```feedgen``` library:

```pip install feedgen```

Install ```feedparser``` library:

```pip install feedparser```

Install ```pytz``` library:

```pip install pytz```

## How to run the program:

On cmd,simply run these commands:

Initialize the database:

```flask --app my_project init-db```

Run the program:

```flask --app my_project --debug```


