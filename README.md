# Trip Split

Trip Split is an application to track trip expenses.

It enables users to seamlessly add, edit, or remove trips and their costs. Additionally, they can gain valuable insights into individual expenditures.

[View the live site here](https://trip-split-b5b1f0cae200.herokuapp.com/)

![Mockup](documentation/readme_images/mockup.png)

## Table of Contents

* [User Goals](#user-goals)
* [Design](#design)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)

## Goals

* Provide an application to track expenses, escpecially for groups.
* It should be intuitive, providing enough information on each step.
* Should give the option, whenever is possible, to option move back to a previous step.
* Should give the option to make changes if a mistake is made.
* It has to provide relevant feedback to the user when there is not enough information or a invalid data is provided.
* It has to calculate the total cost of the trip and how much each person has spent.

### User Stories

* As a user, I want to:
  1. Create a new trip to track expenses.
  2. Be able to have several people adding their expenses to the trip.
  3. Have a currency conversion system to my preferred currency.
  4. See the list of existing trips.
  5. Edit an entry if there was a mistake.
  6. Delete an entry if it was a mistake.
  7. Delete a trip if it was a mistake or is not any more needed.
  8. See how much each person has spent.


## Design

The application has been designed with the goal of having the users making one decision at a time and providing input for it on each step. Whenever possible, they should have the option to move back to the previous step.

### Flowcharts



### Structure

#### Welcome menu
* Displayed when the application is launched. The user will also have the possibility to return to this menu after different interactions.
* Is shows a welcome message and a short explanation of what the user can do.
* Gives the user the possibility to choose between:
    * Create a new trip.
    * See a list of existing trips.

<details><summary>Welcome menu</summary>
<img src="documentation/readme_images/welcome-menu.png">
</details>

#### Create new trip
* It takes the user to the trip creation flow:
    * First, the name of the trip must be provided.
    <details><summary>Create new trip - Name</summary>
    <img src="documentation/readme_images/create-new-trip-name.png">
    </details>

    * Then, the user currency must be provided.
    <details><summary>Create new trip - Currency</summary>
    <img src="documentation/readme_images/create-new-trip-currency.png">
    </details>

    * After those two steps, the trip is created and the user can choose if they want to add an expense.
    <details><summary>Create new trip - Add expense</summary>
    <img src="documentation/readme_images/create-new-trip-expense.png">
    </details>

#### See existing trips
* All trips that have been created are listed.
* The user can choose between one of them or go back to the welcome menu.
<details><summary>See existing trips</summary>
<img src="documentation/readme_images/see-existing-trips.png">
</details>

#### Trip menu
* The number of entries the trip contain are displayed.
* The user has the possibility to:
    * See the trip summary.
    * Edit the trip.
    * Delete the trip.
    * Go back to see the list of trips.
<details><summary>Trip menu - Without entries</summary>
<img src="documentation/readme_images/trip-menu-no-entries.png">
</details>
<details><summary>Trip menu - With entries</summary>
<img src="documentation/readme_images/trip-menu-with-entries.png">
</details>

#### Trip summary
It displays a summary of the trip. From here, the user can only go back to the trip menu.
<details><summary>Trip summary - Without entries</summary>
<img src="documentation/readme_images/trip-summary-no-entries.png">
</details>
<details><summary>Trip summary - With entries</summary>
<img src="documentation/readme_images/trip-summary-with-entries.png">
</details>

#### Edit trip
* It lists all trip entries.
* It gives the possibility to add, edit or delete trip entries. The user can also go back to the trip menu.
<details><summary>Edit trip - Without entries</summary>
<img src="documentation/readme_images/edit-trip-no-entries.png">
</details>
<details><summary>Trip trip - With entries</summary>
<img src="documentation/readme_images/edit-trip-with-entries.png">
</details>

#### Delete trip
* It lists all trip entries.
* Asks for confirmation to delete the trip. The user can either confirm the deletion or go back to the trip menu
<details><summary>Trip summary - Without entries</summary>
<img src="documentation/readme_images/delete-trip-no-entries.png">
</details>
<details><summary>Trip summary - With entries</summary>
<img src="documentation/readme_images/delete-trip-with-entries.png">
</details>


## Features

### User stories fullfillment

1 Create a new trip to track expenses.

    Steps:
    1. Start the programm or navigate back to the welcome menu.
    2. Enter '1' to create a new trip.
    3. Follow the instructions in the next steps:
        - Add a trip name.
        - Choose a currency.

2 Be able to have several people adding their expenses to the trip.

    Steps - Option 1:
    1. After finishing creating a trip, the user will be asked if they want to add an expense. Enter 'Y'
    2. Follow the instructions in each step to create the expense, part of the information to provide is the name of the person adding the expense.
        - Add a date.
        - Add the name of the person.
        - Add the concept.
        - Add the cost.
        - Add the currency.

    Steps - Option 2:
    1. In the welcome menu enter '2' to see the list of existing trips.
    2. Choose the trip for which the expense will be added.
    3. Select 'Edit trip'.
    4. Enter 'A' to add an entry and follow the same steps describe in Option 1.

<details><summary>Add expense - Date</summary>
<img src="documentation/readme_images/add-expense-date.png">
</details>
<details><summary>Add expense - Name</summary>
<img src="documentation/readme_images/add-expense-name.png">
</details>
<details><summary>Add expense - Concept</summary>
<img src="documentation/readme_images/add-expense-concept.png">
</details>
<details><summary>Add expense - Cost</summary>
<img src="documentation/readme_images/add-expense-cost.png">
</details>
<details><summary>Add expense - Currency</summary>
<img src="documentation/readme_images/add-expense-currency.png">
</details>

3 Have a currency conversion system to my preferred currency.

    Steps:
    1. When creating a new trip the user must choose the base currency to which all expenses will be converted to.
    2. When adding a new expense the user must choose the currency they used to pay.
    3. After selecting a trip (Welcome menu > See existing trips > Select trip), enter '1' to see the summary of the trip. The trip cost and cost per person displayed are converted to the currency chosen by the user when the trip was created.

4 See the existing entries of a trip.

    Steps
    1. In the welcome menu, enter '2' to see the list of existing trips.
    2. Enter the number of one of the existing trips.
    3. Select the 'Edit trip' option:
        - If there are no entries, there will be a message saying that the trip is empty.
        - If there are entries, they will be displayed.

5 Edit an entry if there was a mistake.

    Steps - Option 1, While creating the expense:
    1. Follow the steps as described in the User Story 2, entering 'E' instead of 'A'.
    2. Once information for all fields has been provided, a summary of the expense will be displayed.
    3. The user will have the option to edit any of the fields before it is saved:
        - In order to do that, the user must enter the name of the field they want to edit.
        - Then again the summary will be displayed and the user will continue to have the possibility to edit any field.
    4. When all fields have the correct information, the user can save it.

    Steps - Option 2, When the expense already exists:
    1. Follow the steps described in the User Story 4.
    2. Enter 'E'.
    3. Enter the number of the expense to be edited.
    4. The summary of the expense is displayed and it can then be edited in the same way as described in Option 1.

<details><summary>Edit expense</summary>
<img src="documentation/readme_images/edit-expense.png">
</details>

6 Delete an entry if it was a mistake

    Steps:
    1. In the welcome menu enter '2' to see the list of existing trips.
    2. Choose the trip for which the expense will be deleted.
    3. Select 'Edit trip'.
    4. Enter 'D' to delete an entry.
    5. Enter the number of the entry that will be deleted.
    6. Enter 'Y' to confirm.

<details><summary>Delete expense</summary>
<img src="documentation/readme_images/edit-expense.png">
</details>

7 Delete a trip if it was a mistake or is not any more needed.

    Steps:
    1. In the welcome menu enter '2' to see the list of existing trips.
    2. Choose the trip that will be deleted.
    3. Select 'Delete trip'.
    4. Enter 'D' to delete an entry.
    5. Enter 'Y' to confirm.

8 See how much each person has spent.

    Steps:
    1. In the welcome menu enter '2' to see the list of existing trips.
    2. Choose the relevant trip.
    3. Select 'See summary".
    4. The following information will be displayed:
        - The name of the trip.
        - The chosen base currency.
        - The total cost of the trip in the chosen currency.
        - A table with how much each person has spent, how much each person should have paid (total cost / nr. of people) and how much each person should pay (negative numbers) or receive (positive numbers)

### Additional features

#### Data storage

The programm uses a Google Spreadsheet to save and fetch trips data. The spreadsheet can be accessed [here](https://docs.google.com/spreadsheets/d/1bzdwem6NsTVaEm1tRZfcupDeK-qbkPKys-CPtTWXnxc/edit#gid=1855189207).

In order to convert the trip currencies to the base currencies chosen by the users, static currency exchanges have been added to the first worksheet.
<details><summary>Currency exchange</summary>
<img src="documentation/readme_images/currency-exchange.png">
</details>

#### Data model

I've used an Expense class to create the expenses. I first doubted between a dictionary and a class, as I needed a data structure that would allow me to access a value based on a key. The reason I finally decided to use a class is that it would allow me to implement methods to convert the trip currencies to the base currency.

#### Input validation

For each decision users have to make, where input is needed, a validation system has been implemented to make sure users always choose only one of the valid options. For more details see the [Testing](#testing) section.

### Future features

* Users should only be able to see their trips. At the moment only one spreadsheet exists where all trips are stored.
* Add more currencies and a system to dynamically update exchange rates.
* At the moment once the trip currency is set it can't be edited. Add function for users to be able to edit it.
* Add more options to the "See summary" menu. For instance see cost by concept and display charts.


## Technologies Used

### Languages

* Python

### Python libraries and modules

* `gspread` was used for access and manipulation of Google Spreadsheets.
* `google.oauth2.service_account` was used to handle credentials between the application and Google Sheets.
* `os` was used to clear the terminal.
* `datetime` was used to make sure users enter valid dates.
* `time` was used to delay certain actions, as a way to give users a bit more time to better understand what happens.
* `pandas` was used to create dataframes with the data in the spreadsheet. It makes easier to summarize data and do arithmetic operation.
* `colorama` was used to give users visual feedback using colors. 

### Other framewoks and tools
* `CodeAnywhere` was the IDE used to develop the application.
* `GitHub` is used to host the code.
* `Git` was userd for version control.
* `Lucidchart` was used to create the flow charts.
* `Heroku` was used to deploy the project.
* `Patorjk` was used to create the ASCII Art for the welcome message.


## Testing

### Python Linter

### Manual Testing

#### Bugs

| Bug | Solution |
|-----|----------|
| Creating a new trip with the same name as an existing trip caused an error. | Create a new condition that checks if the trip name (worksheet name) already exists. |
| After loading list of existing trips, entering 'C' wasn't accepted as valid input. | Add lower() method to the user's input. |
| Trying to do arithmetic operation with data from spreadsheet caused an error. | Add the replace() method to change ',' with '.' and convert the result to float. |
| Trying to see the summary of an empty trip caused an error. | Check first if the trip is empty before performing operations. If it's empty only display a message. |
| After deleting a trip, the deleted trip was still being displayed if the user chose to see existing trips right after deleting it, causing an error. | The worksheets were being loaded in the global scope, so they weren't update unless the user restarted the application. I moved the variable to the local scope of the functions that needed access to it. | 
| An empty trip (without header) could be created if the user aborted the trip creation process after entering the name of the trip and cancelled before selecting the base currency. This would result in errors when trying to select the trip later on. | Move the worksheet creation method call until after the user has provided all necessary information. And add exception handling to the get_currency function if the user canceled before entering the currency (because otherwise the load_trip function would try to load a non existing trip). |
| Trying to see the summary of a trip with only 1 entry caused an error. | I made a mistake and was assigning to the `chosen_curr` varibale the index 1 instead of 0 of the dataframe. |


## Deployment


## Credits