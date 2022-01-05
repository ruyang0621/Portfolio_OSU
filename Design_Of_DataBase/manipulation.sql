-- Manage Authors
-- Add Authors
INSERT INTO Authors (firstName, lastName) VALUES (:firstNameAddInput, :lastNameAddInput);

-- Search Authors
SELECT * FROM Authors WHERE firstName = :firstNameSearchInput AND lastName = :lastNameSearchInput;

-- Update Authors
UPDATE Authors SET firstName = :firstNameUpdateInput, lastName = :lastNameUpdateInput WHERE authorId = :author_ID_from_the_list;

-- Delete Authors
DELETE FROM Authors WHERE authorId = :author_ID_from_the_list;


-- Manage Categories
-- Add Categories
INSERT INTO Categories (categoryName) VALUES (:categoryNameAddInput);

-- Search Categories
SELECT * FROM Categories WHERE categoryName = :categoryNameSearchInput;

-- Update Categories
UPDATE Categories SET categoryName = :categoryNameUpdateInput WHERE id= :category_ID_from_the_list;

-- Delete Categories
DELETE FROM Categories WHERE categoryId = :category_ID_from_the_list;


-- Manage Books
-- Add Books (Please remember to add Copies, BooksAuthors, and BooksCategories after adding base book info).
INSERT INTO Books (ISBN, publisher, title, publicationYear) 
VALUES (:isbnAddInput, :publisherAddInput, :titleAddInput, :publicationYearAddInput);

-- Search Books
SELECT * FROM Books WHERE title = :bookSearchInput OR ISBN = :bookSearchInput;

-- Update Books.
UPDATE Books SET ISBN = :isbnUpdateInput, publisher = publisherUpdateInput, title = titleUpdateInput,
publicationYear = publicationYearUpdateinput WHERE id= :book_ID_from_the_list;

-- Delete Books (when a book is deleted, the corresponding copy versions 
-- book_author and book_category relationships will be removed as well).
DELETE FROM Books WHERE bookId = :book_ID_from_the_list;


-- Manage BooksAuthors
-- Add BooksAuthors (bookId and authorId need to be search at first).
INSERT INTO BooksAuthors (bookId, authorId) VALUES (:bookIdAddInput, :authorIdAddInput);

-- Search BooksAuthors
SELECT * FROM BooksAuthors WHERE bookId= :book_author_search_input OR authorId= :book_author_search_input;

-- Update BooksAuthors (Only updated authorId and authorId need to be search at first).
UPDATE BooksAuthors SET authorId = :authorIdUpdateInput WHERE bookId= :book_ID_from_the_list;

-- Delete BooksAuthors 
DELETE FROM BooksAuthors WHERE bookId = :book_ID_from_the_list;


-- Manage BooksCategories
-- Add BooksCategories (bookId and categoryId need to be search at first).
INSERT INTO BooksCategories (bookId, categoryId) VALUES (:bookIdAddInput, :categoryIdAddInput);

-- Search BooksCategories
SELECT * FROM BooksCategories WHERE bookId= :book_category_search_input OR categoryId= :book_category_search_input;

-- Update BooksCategories (Only updated categoryId and categoryId need to be search at first).
UPDATE BooksCategories SET categoryId = :categoryIdUpdateInput WHERE bookId= :book_ID_from_the_list;

-- Delete BooksCategories 
DELETE FROM BooksCategories WHERE bookId = :book_ID_from_the_list;



-- Manage copies
-- Add Book Copies by user. The bookId need to be search at first.
INSERT INTO Copies (bookId, copyNum, bookCondition, status) VALUES (:bookIdInput, :conditonInput,:statusInput)

-- Search Book Copy by Copy ID.
SELECT copyId, bookId, copyNum, condition, status FROM Copies WHERE copyId = :copyIdInput

--Update the copy record
UPDATE Copies SET bookId = :bookIdInput, copyNum = :copyNumInput, condition= :conditonInput, status = :statusInput WHERE copyId = :copy_ID_from_the_list

-- Delete a copy
DELETE FROM Copies WHERE copyId = :copy_ID_from_the_list


-- Manage Borrow Records
-- Add Borrow Records
INSERT INTO BorrowRecords (memId, copyId,borrowDate, dueDate) VALUES (:memIdInput, :copyIdInput,:borrowDateInput,:dueDateInput)

-- Search Borrow Records by Member ID
SELECT borrowId, copyId, borrowDate, dueDate, passDue FROM BorrowRecords WHERE memId = :memIdInput

--Update a borrow record
UPDATE BorrowRecords SET memId = :memIdInput, copyId = :copyIdInput, borrowDate= :borrowDateInput, dueDate = :dueDateInput WHERE borrowId= :borrow_ID_from_the_list

-- Delete a borrow record
DELETE FROM BorrowRecords WHERE borrowId = :borrow_ID_from_the_list


-- Manage Members
-- Add new member
INSERT INTO Members (firstName, lastName,memAddress, memEmail, memCell) VALUES (:firstNameInput, :lastNameInput,:memAddressInput,:memEmailInput,:memCellInput)

-- Search Member by Name
SELECT firstName, lastName,memAddress, memEmail, memCell FROM Members WHERE firstName = :firstNameInput AND lastName = :lastNameInput

--Update member record
UPDATE Members SET firstName = :firstNameInput, lastName = :lastNameInput, memAddress= :addressInput, memEmail = :emailInput, memCell = :cellInput WHERE memId= :member_ID_from_the_list

-- Delete a copy
DELETE FROM Members WHERE memId = :member_ID_from_the_list
