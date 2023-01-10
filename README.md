# Flask-Forum
Forum created in flask

## Features

1. Register users
2. Login users
3. Create new posts
4. Edit posts
5. Show outside post info
6. Show inside post info
7. Do real-time 'like' or 'dislike' to post 
8. Do real-time comment to post 
9. Edit comment
10. Navigation pages
11. Option to choose how many posts per page
12. Marking tag when hover on that tag
13. Filter posts by name
14. Filter posts by tag
15. RSS feed for new posts

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

```flask --app my_project init-db```

Then run this:

```flask --app my_project --debug```


