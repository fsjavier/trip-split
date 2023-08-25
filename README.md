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

### User Goals

* As a user, I want to:
  1. Create a new trip to track expenses.
  2. Be able to have several people adding their expenses to the trip.
  3. Have a currency conversion system to my preferred currency.
  4. See the existing entries of a trip.
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

## Features
