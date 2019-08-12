# Instructions

We would like to see how you solve an OO design problem. Let's create a simple subscription system.
**The goal is to emulate buying a yearly plan and attach website(s) to it.**

There are 3 business entities :

- Customer - has a name, a password an email address, a subscription and a subscription renewal date.
- Plan - has a name, a price, and a number of websites allowance.
- Website - has an URL, and a customer


A customer should be able to subscribe to plan, move from a plan to another and manage websites (add/update/remove) according to his plan.
Subscriptions have a 1-year time value.



Notes :
- Having a DB is optional
- We have 3 plans :
	- Single, 1 website, 49$
	- Plus, 3 websites $99
	- Infinite, unlimited websites $249


- Please add automated tests, using unittest


## todo

* Add tests - Done
* initialise Plans - example script to demo functionality (also tests)
* customer to subscribe to a plan - can a customer exist without a plan?
* customer to move to another plan - Done
* add website (check plan if available) - Done
* update website (URL) - Done
* remove website - Done

* hash the password securely
