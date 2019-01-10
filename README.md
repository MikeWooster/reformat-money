# Reformat Money

`reformat-money` is a simple command line utility that will attempt to
reformat the usage of [`py-moneyed`][py-moneyed] Money within the application
into a standard string format.

The driver behind this is that usage of money within an application needs to
be consistent and precise.  The main aim of this utility is to stop an
application defining money as `float`, which can lead to unpredictable errors.
In order to keep consistency, where possible all instances of money will have
the amount reformatted to a string.

The following will be reformatted.
```
Money(100.20, "USD") --> Money("100.20", "USD")
Money(200, "USD") --> Money("200.00", "USD")
```

If it is not possible to reformat, the filename will be logged for the user to
inspect manually.

It is advised that you have your code committed to version control before running
`reformat-money` to allow you to roll back changes that you are not happy with.


## Installation

Installation is simple:
```
pip install reformat-money
```

## Usage

This utility can be used by specifying either a single file or directory, for example

```
reformat-money package_name
```


[py-moneyed]: https://github.com/limist/py-moneyed