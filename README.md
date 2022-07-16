# field-transformer
- Rename columns in a dataframe (renames)
- Create new calculated columns (transformations)
- Output a dataframe in the desired column structure (structure)

The module performs operations on Pandas DataFrames and wraps some of its methods to implement the desired functionality.

## How to use this module.
The module supplies a `Transformer` class through which all operations are performed.

To use the `Transformer` class, instantiate an object:
```
transformer = Transformer()
```

There are 3 operations the `transformer` can perform - given by the arguments to it's `__call__` method. It must be called with a Pandas DataFrame as the argument `df`, and the following:
- `transformations` defines any calculated columns to create,
- `renames` defines columns to rename,
- `structure` defines the output

To perform these operations on the dataframe, call the `transformer` like this:

```
transformer(
    df=dataframe_to_transform,
    transformations=transformations_to_make,
    renames=column_names_to_change,
    structure=desired_output_column_names
)
```

The transformer will set its `transformed_df` and `transformed_df_as_dicts` using the resultant dataframe.

Retrieve these by doing:

```
transformed_df = transformer.transformed_df
transformed_df_as_dicts = transformer.transformed_df_as_dicts
```

The shape and values of these arguments need to be of a specific form. The operations and their format are described in more detail below.
### tranformations
Transformations or calculations can be performed on each row.

For example, the following operation creates `a_new_column` by applying the `divide` operation to the columns `column_a` and `column_b`. The key `a_new_column` defines the column name, and the output of its value (in the key:value sense) gives its value.
```
{
    "a_new_column": {
        "operation": "divide",
        "columns": {
            "numerator": "column_a",
            "denominator": "column_b"
        },
    }
}
```
Calculations can involve intermediate steps, too. These are calculated first. This is done by specifying `steps`.

The following operation has an intermediate step to create the column `sum_a_b`. This operation sums the values of `column_a` and `column_b` to create the column `sum_a_b`. This column is then used in its parent calculation to create `a_new_column` by dividing `sum_a_b` by the constant 2.0.
```
{
    "a_new_column": {
        "operation": "divide",
        "columns": {
            "numerator": "sum_a_b",
            "denominator": 2.0
        },
        "steps": {
            "sum_a_b" {
                "operation": "sum",
                "columns": ["column_a", "column_b"]
            }
        }
    }
}
```

### renames
This argument defines which existing columns to rename, and what to rename them to. This is done using key:value pairs where the key is the existing column name, and the value is the renamed column.

For example, if the following was passed to the transformer's `renames` argument, the column `column_a` would be renamed to `Column Ay` and `column_b` to `Column Bee`, in the resultant dataframe.
```
{
    "column_a": "Column Ay",
    "column_b": "Column Bee"
}
```

### structure
This argument defines the columns to be included in the resultant dataframe.

For example, if a dataframe with columns `column_a`, `column_b` and `column_c` was provided to the transformer, and an output of just `column_a` and `column_c` was desired, the following would be passed as the `structure` argument.
```
[
    "column_a",
    "column_c"
]
```