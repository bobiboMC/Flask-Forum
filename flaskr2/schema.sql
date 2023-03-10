DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  liked_posts DEFAULT "(-1)",
  disliked_posts DEFAULT "(-1)" 
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  tag TEXT,
  likes INTEGER DEFAULT 0,
  dislikes INTEGER DEFAULT 0,
  thumbnail TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  body Text NOT NULL,
  created DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP,'LOCALTIME')),	
  publisher_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  FOREIGN KEY (publisher_id) REFERENCES user (id),
  FOREIGN KEY (post_id) REFERENCES post (id)
);
