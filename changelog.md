## [18.0.1.1.0] 2025-03-17

- new fields were added into the sale_order
- override the action_confirm method
- inherit the view and change visibility of confirmation button and add two new buttons Approve and Reject
- improve code and verify the test case
- add changelog.md file

## [18.0.2.1.1] 2025-03-17

- add new button into the product template on that button add new wizard
- add a new wizard model and normal to store the wizard model's data
- add two new views, one for the wizard model and the other for the normal model

## [18.0.2.2.0] 2025-03-21

- add the new template action to create and download the qweb report of a library

## [18.0.2.3.0] 2025-03-21

- add new server action to notify that the book is returned
- add new action to acknowledge the borrower that he/she borrow a book
- add a new automated action that checks the borrower's history and stops borrowing new books

## [18.0.2.4.0] 2025-03-21

- add a new SQL constraint for the library to avoid the duplicate name of a library
- add a new python constraint for borrow transaction history to stop borrowing the already borrowed books
- implement the chatter into the product template to receive a notification that who borrow the book
- make a new activity for the librarian to remind a return a book 
