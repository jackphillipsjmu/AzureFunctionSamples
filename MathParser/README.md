# Math Parser
Takes in a JSON or URL form encoded payload containing a parameter, `calculation` that stores in a String mathematical expression such as, `2 + 2`. It will evaluate the request and perform the calculation if it can do so. The response for invoking clients, given you provided `2 + 2` to the `calculate` field is
```
{
  "expression": "2 + 2",
  "result": 4
}
```

## Test out the Functionality

### Use JSON Payload
The following `cURL` statement will pass along the mathematical expression `2 * 2 + 2` which should equal `6` in a JSON payload. All you will have to do is specify the JSON data with the appropriate `calculate` key and math expression value to calculate.

###### Command
`curl -X POST -H "Content-Type:application/json" --data '{"calculate":"2 * 2 + 2"}' http://localhost:7071/api/MathParser`

###### Result
```
{
  "expression": "2 * 2 + 2",
  "result": 6
}
```

### Use Form Parameters
The following `cURL` statement will pass along the mathematical expression `(2 * 2 + 2) / 2` which should equal `3`. Just provide the `calculate=(2 * 2 + 2) / 2` form parameter and receive the computed math expression.

###### Command
`curl -X POST http://localhost:7071/api/MathParser -F 'calculate=(2 * 2 + 2) / 2'`

###### Result
```
{
  "expression": "(2 * 2 + 2) / 2",
  "result": 3
}
```
