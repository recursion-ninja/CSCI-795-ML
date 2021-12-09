## JSON Extractor

### A tool for flattening 5e.tools magic item JSON file


#### Building `json-extractor`

  1.  Install the [Haskell] build tool [`cabal` ][cabal]

  2.  Build the project by invoking the following command:

      `cabal install`


#### Using `json-extractor`

The JSON Extractor expects a list of key value pairs.
The input list can be specified via either the `-i` or `--input` flags.
The input list has syntax of the following form:

```
'[ (key0, value0), (key1, value1), ... (keyN, valueN) ]'
```

Each value represents a double-quoted path to a JSON file containing magic items.

Each key represents a double-quoted field of the JSON object containing the magic item(s) within the corresponding JSON file. If the corresponding JSON file contains a only a magic item object or array of magic item objects which does not need to be indexed from a containing object, the empty key of `""` can be supplied.

An example invocation of `json-extractor`:

```
$ json-extractor -i '[("baseitem","../items-base.json"), ("item","../items.json")]'
```

This invocation will write the flattened JSON file(s) contents to a 'magic-items.csv' file in the working directory.
Optionally, a different file path can be supplied with either the '-o' or '--output` flags.

[haskel]: https://www.haskell.org/
[cabal ]: https://www.haskell.org/cabal/download.html