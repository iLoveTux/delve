Delve is a toolkit designed to help facilitate working with data.

Delve follows an eventual-schema philosophy, where you do not need a schema to 
get started working with the data. Simply index your data to get started.

Delve allows you to index arbitrary pieces of data as Events. An Event is a
piece of data. Events have four Indexed Fields to help making searching faster:

* Index - The name of the index to which this event belongs
* host - The hostname of the computer from which this event originated
* source - The source of the event (ie. dpkg)
* sourcetype - The type of event corresponding to the source


