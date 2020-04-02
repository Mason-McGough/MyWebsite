DROP TABLE IF EXISTS post;

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  date_posted TIMESTAMP NOT NULL,
  thumbnail TEXT NOT NULL,
  filename TEXT NOT NULL
);

INSERT INTO post (title, description, date_posted, thumbnail, filename)
VALUES
  (
      'Welcome',
      'An introduction to the creation of this website',
      '2018-02-17 00:00:00.000',
      'welcome/welcome-thumbnail.jpg',
      'welcome.html'
  ),
  (
    'Setting Up This Server',
    'How and why I created the server running this website',
    '2018-02-25 00:00:00.000',
    'setting-up-this-server/setting-up-this-server-thumbnail.png',
    'setting-up-this-server.html'
  ),
  (
    'Operations Graph',
    'A method for running function operations in sequence with piped outputs',
    '2018-05-07 00:00:00.000',
    'operations-graph/operations-graph-thumbnail.png',
    'operations-graph.html'
  ),
  (
    'Multivariable Calculus with Python',
    'A review of fundamental multivariable calculus concepts with Python and Jupyter notebooks',
    '2018-08-21 00:00:00.000',
    'multivariable-calculus/multivariable-calculus-thumbnail.png',
    'multivariable-calculus.html'
  );