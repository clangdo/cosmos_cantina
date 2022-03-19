# Cosmo's Cantina

**IMPORTANT SECURITY INFORMATION** This project was created for a university course and it lacks any kind of authentication. If you intend to run it please note that it is totally unsecure. We also use home grown validation and sanitization which should NOT be relied upon. If you're looking for a production ready database solution for your bar *this is NOT it*, please don't even attempt to set this up if you don't know what you're doing.


Welcome to the Andromeda Galaxy's premier establishment. This is where the finest drinks are sorted, indexed and inventoried.

## Using

### Dependencies
- `python3`
- `Flask`
- `mariadb` (the official python connector)

We recommend using a python virtual environment `app/env` to run the frontend. This is subject to change, and the frontend folder may promote to the root folder in the future.

Once you have dependencies installed, go ahead and run the flask development server with `flask run`, if you'd like the debugger enabled (which you should be careful about for security reasons as stated in the [flask quickstart guide](https://flask.palletsprojects.com/en/2.0.x/quickstart/), then you can append `FLASK_ENV=development` to your environment variables before running the server.

### Features
Our database's basic concept is detailed on the homepage (there is a link to the homepage in the footer if you navigate away).

We have a bibliography for works referenced on another page you can get to via the footer.

We have five tables, customers, drinks, ingredients, purchases, and tabs. The ingredients table
implements the many-to-many recursive relationship drinks have with themselves.

Purchases is also an intersection between tabs and drinks, we recommend using the filters to isolate a
particular customer.

All of the filters have suggestion lists populated from the tables, and you should be able to use them jointly
to AND the filter.

You can view, edit, update, and delete everything. There are slightly different semantic behaviors depending
on what you're doing.

- For our many to many ingredients relationship, you can view the ingredients list for each drink by going to the drinks table (labeled "inventory") and clicking on the appropriate ingredients button in the table.
- When you create or edit a purchase, ingredients are automatically deducted/replaced based what you did.
- However, when you delete a purchase ingredients are not modified.
- Our validation should prevent you from entering most invalid values, and give you feedback as to what's wrong. This includes cyclic drinks ingredient references, which should not be possible.
- The "UBA Number" for a customer must be a 20 character string after quoting, there are no other restrictions for its contents.
- "Super Cocktails", with cocktails as ingredients are supported at a technical level, but are not recommended due to user experience reasons.

No guarantees are made with respect to the efficiency of the design.

## Contributing

Please conform to PEP 8.

Please adhere to the following guidelines when writing
commit messages.

In particular:
- Write the commit subject in the imperative voice.
- Begin the commit subject with a capitalized verb.
- Do not add periods to fragments or the commit subject.
- Leave one empty line between the subject and further explanation.
- Keep the subject short.

Also, only include information that the diff does not clearly indicate. Technical information written in English often simply muddies the water. That said, you should write a bit about the reasoning for architecture changes. You should also explain controversial changes, or anything that's hard to grasp just by looking at the code. Having a brief high level introduction of a new pattern or code structure is also a good idea where applicable.
