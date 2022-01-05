DROP TABLE IF EXISTS Books;
CREATE TABLE Books (
    bookId int NOT NULL AUTO_INCREMENT,
    ISBN varchar(13) NOT NULL UNIQUE,
    publisher varchar(150) NOT NULL,
    title varchar(255) NOT NULL,
    publicationYear year NOT NULL,
    PRIMARY KEY (bookId)
);

DROP TABLE IF EXISTS Authors;
CREATE TABLE Authors (
    authorId int NOT NULL AUTO_INCREMENT,
    firstName varchar(50) NOT NULL,
    lastName varchar(50) NOT NULL,
    PRIMARY KEY (authorId),
    CONSTRAINT author_cst UNIQUE (firstName, lastName)
);

DROP TABLE IF EXISTS Categories;
CREATE TABLE Categories (
    categoryId int NOT NULL AUTO_INCREMENT,
    categoryName varchar(50) NOT NULL UNIQUE,
    PRIMARY KEY (categoryId)
);

DROP TABLE IF EXISTS BooksAuthors;
CREATE TABLE BooksAuthors (
    bookId int,
    authorId int,
    PRIMARY KEY (bookId, authorId),
    FOREIGN KEY (bookId) REFERENCES Books(bookId),
    FOREIGN KEY (authorId) REFERENCES Authors(authorId)
);

DROP TABLE IF EXISTS BooksCategories;
CREATE TABLE BooksCategories (
    bookId int,
    categoryId int,
    PRIMARY KEY (bookId, categoryId),
    FOREIGN KEY (bookId) REFERENCES Books(bookId),
    FOREIGN KEY (categoryId) REFERENCES Categories(categoryId)
);

DROP TABLE IF EXISTS Copies;
CREATE TABLE Copies (
    copyId int NOT NULL AUTO_INCREMENT,
    bookId int NOT NULL,
    copyNum int NOT NULL CHECK (copyNum > 0 and copyNum < 4),
    bookCondition varchar(15) NOT NULL CHECK (bookCondition in ('new', 'very_good', 'good', 'fair', 'need_replaced')),
    status varchar(10) DEFAULT('in Library') CHECK (status in ('on loan', 'in Library')),
    PRIMARY KEY(copyId),
    FOREIGN KEY (bookId) REFERENCES Books(bookId),
    CONSTRAINT book_copy UNIQUE (bookId, copyNum)
);

DROP TABLE IF EXISTS Members;
CREATE TABLE Members (
    memId int NOT NULL AUTO_INCREMENT,
    firstName varchar(50) NOT NULL,
    lastName varchar(50) NOT NULL,
    memAddress varchar(50) NOT NULL,
    memEmail varchar(255) NOT NULL UNIQUE,
    memCell varchar(10) NOT NULL,
    PRIMARY KEY (memId),
    CONSTRAINT member_cst UNIQUE (firstName, lastName, memCell)
);

DROP TABLE IF EXISTS BorrowRecords;
CREATE TABLE BorrowRecords (
    borrowId int NOT NULL AUTO_INCREMENT,
    memId int NOT NULL,
    copyId int NOT NULL,
    borrowDate date NOT NULL,
    dueDate date NOT NULL,
    passDue boolean NOT NULL,
    PRIMARY KEY (borrowId),
    FOREIGN KEY (memId) REFERENCES Members(memId),
    FOREIGN KEY (copyId) REFERENCES Copies(copyId)
);

-- Part B
INSERT INTO Books (ISBN, publisher, title, publicationYear)
VALUES
  (
    '9780441172719',
    'Ace Books',
    'Dune',
    1965
  ),
  (
    '9780812550702',
    'Tor Book',
    "Ender's Game",
    1985
  ),
  (
    '9780345391803',
    'Del Rey',
    "The Hitchhiker's Guide to the Galaxy",
    1979
  ),
  (
    '9780451524935',
    'Houghton Mifflin Harcourt',
    '1984',
    1949
  ),
  (
    '9781451673319',
    'Simon & Schuster',
    'Fahrenheit 451',
    1953
  );


INSERT INTO Authors (firstName, lastName)
VALUES
  (
    'Frank',
    'Herbert'
  ),
  (
    'Orson Scott',
    'Card'
  ),
  (
    'Douglas',
    'Adams'
  ),
  (
    'Thomas',
    'Tidholm'
  ),
  (
    'Eoin',
    'Colfer'
  ),
  ( 'George',
    'Orwell'
  ),
  (
    'Ray',
    'Bradbury'
  );


INSERT INTO Categories (categoryName)
VALUES
    (
      'Novel'
    ),
    (
      'Science Fiction'
    ),
    (
      'Comedy'
    ),
    ( 
      'Dystopian Fiction'
    );


INSERT INTO BooksAuthors (bookId, authorId)
VALUES
    (
      (SELECT bookId from Books WHERE title='Dune'),
      (SELECT authorId from Authors WHERE firstName='Frank' AND lastName="Herbert")
    ),
    (
      (SELECT bookId from Books WHERE title="Ender's Game"),
      (SELECT authorId from Authors WHERE firstName='Orson Scott' AND lastName="Card")
    ),
    (
      (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
      (SELECT authorId from Authors WHERE firstName='Douglas' AND lastName="Adams")
    ),
    (
      (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
      (SELECT authorId from Authors WHERE firstName='Thomas' AND lastName="Tidholm")
    ),
    (
      (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
      (SELECT authorId from Authors WHERE firstName='Eoin' AND lastName="Colfer")
    ),
    (
      (SELECT bookId from Books WHERE title='1984'),
      (SELECT authorId from Authors WHERE firstName='George' AND lastName="Orwell")
    ),
    (
      (SELECT bookId from Books WHERE title='Fahrenheit 451'),
      (SELECT authorId from Authors WHERE firstName='Ray' AND lastName="Bradbury")
    );


INSERT INTO BooksCategories (bookId, categoryId)
VALUES
    (
      (SELECT bookId from Books WHERE title='Dune'),
      (SELECT categoryId from Categories WHERE categoryName='Novel')
    ),
    (
      (SELECT bookId from Books WHERE title="Ender's Game"),
      (SELECT categoryId from Categories WHERE categoryName='Science Fiction')
    ),
    (
      (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
      (SELECT categoryId from Categories WHERE categoryName='Science Fiction')
    ),
    (
      (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
      (SELECT categoryId from Categories WHERE categoryName='Comedy')
    ),
    (
      (SELECT bookId from Books WHERE title='1984'),
      (SELECT categoryId from Categories WHERE categoryName='Dystopian Fiction')
    ),
    (
      (SELECT bookId from Books WHERE title='Fahrenheit 451'),
      (SELECT categoryId from Categories WHERE categoryName='Science Fiction')
    ),
    (
      (SELECT bookId from Books WHERE title='Fahrenheit 451'),
      (SELECT categoryId from Categories WHERE categoryName='Dystopian Fiction')
    );


INSERT INTO Copies (bookId, copyNum, bookCondition, status)
VALUES
  (
    (SELECT bookId from Books WHERE title='Dune'),
    1,
    'new',
    'on Loan'
  ),
  (
    (SELECT bookId from Books WHERE title='Dune'),
    2,
    'very_good',
    'in Library'
  ),
  (
    (SELECT bookId from Books WHERE title='Dune'),
    3,
    'new',
    'on Loan'
  ),
  (
    (SELECT bookId from Books WHERE title="Ender's Game"),
    1,
    'new',
    'in Library'
  ),
  (
    (SELECT bookId from Books WHERE title="Ender's Game"),
    2,
    'new',
    'on Loan'
  ),
  (
    (SELECT bookId from Books WHERE title="Ender's Game"),
    3,
    'good',
    'in Library'
  ),
  (
    (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
    1,
    'new',
    'on Loan'
  ),
  (
    (SELECT bookId from Books WHERE title="The Hitchhiker's Guide to the Galaxy"),
    2,
    'new',
    'in Library'
  ),
  ( 
    (SELECT bookId from Books WHERE title='1984'),
    1,
    'new',
    'on Loan'
  ),
  (
    (SELECT bookId from Books WHERE title='1984'),
    2,
    'new',
    'in Library'
  ),
  ( 
    (SELECT bookId from Books WHERE title='1984'),
    3,
    'new',
    'in Library'
  ),
  ( 
    (SELECT bookId from Books WHERE title='Fahrenheit 451'),
    1,
    'new',
    'in Library'
  ),
  ( 
    (SELECT bookId from Books WHERE title='Fahrenheit 451'),
    2,
    'very_good',
    'on Loan'
  ),
  ( 
    (SELECT BookId from Books WHERE title='Fahrenheit 451'),
    3,
    'new',
    'in Library'
  );


INSERT INTO Members (firstName, lastName, memAddress, memEmail, memCell)
VALUES
  (
    'Edward',
    'King',
    '23 Planet Street, 51 District, Moon City',
    'eking@mooncity.com',
    '9991111111'
  ),
  (
    'Francis',
    'William',
    '123 Luna Street, 51 District, Moon City',
    'fking@mooncity.com',
    '9991111112'
  ),
  (
    'Stephen',
    'Jones',
    '77 Universal Road, 51 District, Moon City',
    'sking@mooncity.com',
    '9991111113'
  ),
  (
    'Noah',
    'Gracia',
    '32 Edward Road, 51 District, Moon City',
    'nGracia@mooncity.com',
    '9991111114'
  ),
  (
    'James',
    'Miller',
    '32 King Drive, 51 District, Moon City',
    'jMiller@mooncity.com',
    '9991111115'
  );


INSERT INTO BorrowRecords (memId, copyId, borrowDate, dueDate, passDue)
VALUES
  (
    (SELECT memId from Members WHERE firstName='Edward' AND lastName='King'),
    1,
    '2047-01-01',
    '2047-01-14',
    FALSE
  ),
  (
    (SELECT memId from Members WHERE firstName='Francis' AND lastName='William'),
    3,
    '2047-01-01',
    '2047-01-14',
    FALSE
  ),
  (
    (SELECT memId from Members WHERE firstName='James' AND lastName='Miller'),
    13,
    '2047-01-01',
    '2047-01-14',
    FALSE
  ),
  (
    (SELECT memId from Members WHERE firstName='Noah' AND lastName='Gracia'),
    7,
    '2047-01-07',
    '2047-01-21',
    FALSE
  ),
  (
    (SELECT memId from Members WHERE firstName='Stephen' AND lastName='Jones'),
    9,
    '2047-01-07',
    '2047-01-21',
    FALSE
  ),
  (
    (SELECT memId from Members WHERE firstName='Edward' AND lastName='King'),
    5,
    '2046-12-01',
    '2047-12-14',
    TRUE
  );
