# linkml-cim-with-ucum
The goal is to have a linkml schema of CIM, but without nested attributes. 

## The problem of nested attribute
In the current schema, quantities are objects:

```yml
classes:
    Structure:
        attributes:
            height:
                range: Length

    Length:
        class_uri: cim:Length
        description: Unit of length. It shall be a positive value or zero.
        attributes:
            multiplier:
                slot_uri: cim:Length.multiplier
                range: UnitMultiplier
            unit:
                slot_uri: cim:Length.unit
                range: UnitSymbol
            value:
                slot_uri: cim:Length.value
                range: float
```

In this repository, the nested attributes are converted to decimals with units. For the `Length` example, this is the result:

```yml
classes:
    Structure:
        attributes:
            height:
                range: decimal
                unit:
                    ucum_code: m
```

## Steps
In `main.py`, these steps are done:

1. Read the CIM LinkML schema from here: https://github.com/Netbeheer-Nederland/im-tc57cim/
2. Find all classes that represent quantities (i.e. classes that have only three attributes `value`, `multiplier`, `unit`). These are now reffered as "quantity classes".
3. Replace all attributes in all classes that have a quantity class as range. The new range is decimal, and the unit is taken from the `cim-quantities-to-ucum.yml` mapping.
4. Delete the quantity classes.
5. Save the new schema.