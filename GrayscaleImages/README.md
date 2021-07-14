# Gray Scale Images Azure Function
Example HTTP Azure Function that will take in either a URL form encoded request payload containing `1..N` images or a single image using binary data. The function will transform the data into a gray scale image(s), and respond with an in-memory `zip` file that contains the results. These outputs could be stored to a local filesystem, ingested by another function or service and more!

## Prerequisites
- Download [.NET Core](https://dotnet.microsoft.com/download) if you do not have it already and install it.
- Install [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash#v2) to your local machine.
- For testing out using cURL make sure you have a terminal capable of running `curl` commands. If you don't your could utilize something such as Postman or other ways to send HTTP requests.

## Creating the Function Using Command Line
- Create the Base Project (not needed if pulling in repo): `func init AzureFunctionSamples --python`
- Change into the Base Project directory: `cd AzureFunctionSamples`
- Create a new function: `func new --name GrayscaleImages --template "HTTP trigger" --authlevel "anonymous"`
- Update the `local.settings.json` file with the following,
```
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": ""
  },
  "Host": {
    "LocalHttpPort": 7071,
    "CORS": "*",
    "CORSCredentials": false
  }
}
```
- Start the function: `func start`
- Open a new terminal/command line window to initiate test requests and go into the `AzureFunctionSamples` directory.

## Test out the Functionality in Two Ways
You can either submit a URL form encoded request to the HTTP trigger, or, you can also submit binary data for a single image. Each request can consume the following request parameters OR form parameters when applicable:
- `include_timestamp`: String value to determine whether to append a timestamp to the file name. For values `y, yes, t, true, on and 1` it will map to True, while `n, no, f, false, off and 0` maps to False. This will default to `False` if nothing is specified.
- `default_image_name`: Override default file name if we cannot determine the file name in code. This seen when binary data is submitted to the function that is NOT utilizing Form inputs. This will default to `default_img.png` if nothing is specified.

For testing, we will be using cURL commands utilizing test image files in this repository located in the `AzureFunctionSamples/test_img` directory. the URL endpoint that will be invoked is `http://localhost:7071/api/GrayscaleImages`. Also, we specify `-o ZIP-FILE-NAME.zip` to store the output to the local filesystem to be examined by who ever is using this code.

### Testing out Single Image File using Binary Data
_**Note**: Do not supply and form parameters when supplying binary data you can only use request parameters for this use case._

#### No Request Parameters
Supplies a PNG image to the function and does not specify any special parameters. These will then assume default values for each specified above which means it will not append a timestamp and will use the default name.  This produce a `zip` file, `output-binary-without-timestamp-and-default-name.zip` which when it is unzipped contains an image `default_img.png`
###### Command
`curl --data-binary @./test_img/patchy_input.png http://localhost:7071/api/GrayscaleImages -o output-binary-without-timestamp-and-default-name.zip`

#### With Request Parameters
Supplies a PNG image to the function and specified that it wants to have the `default_image_name` set to `foo_image.png` and that we would like a timestamp in the filename since `include_timestamp` is set to `Y`. The result of this should make a `zip` file with the name `output-binary-with-timestamp-and-override-name.zip` and once unzipped a file similar to this name will be extracted `foo_image-20210714-153329.png`.
###### Command
`curl --data-binary @./test_img/patchy_input.png 'http://localhost:7071/api/GrayscaleImages?default_image_name=foo_image.png&include_timestamp=Y' -o output-binary-with-timestamp-and-override-name.zip`

### Testing out Processing with Form Data

#### Single Image as Form Parameter
Supplies a PNG image to the function and specifies that the `images` form parameter is set to our image data we want to pass in. This will produce a `zip` file, `output-single-image.zip` containing a single image once unzipped, `patchy_input.png`/

###### Command
`curl -X POST 'http://localhost:7071/api/GrayscaleImages' -F 'images=@./test_img/patchy_input.png' -o output-single-image.zip`

#### Multiple Images With Form Parameters
Supplies multiple images to the function and provides the form parameter, `include_timestamp` which is set to `Y` so we will include timestamps in the output. Finally, an array of pictures is supplied with the `'images[0]=@./test_img/patchy_input.png'` and `'images[1]=@./test_img/patchy_other.jpg'` form parameters. Basically, it will create an array `images[]` and you put the relevant files in there, `images[index]=@/path/to/your/image.png`. This produces a `zip` file, `output-zip-multi-img-with-timestamps.zip` and once unzipped will have two files in the directory similarly names to, `patchy_input-20210714-160232.png` and `patchy_other-20210714-160232.jpg`

###### Command
`curl -X POST 'http://localhost:7071/api/GrayscaleImages' -F 'include_timestamp=Y' -F 'images[0]=@./test_img/patchy_input.png' -F 'images[1]=@./test_img/patchy_other.jpg' -o output-zip-multi-img-with-timestamps.zip`

#### Mixing Request and Form Parameters
Supplies multiple images to be function. This utilizes the `include_timestamp` as a request parameter which is set to `N` so timestamps won't be appended to result file names. In addition, it has other form parameters that can be used that are also request parameters, namely, `default_image_name` which won't do much since we can determine the file names in the Python code but is good to show as an example. This produces a `zip` file, `output-zip-multi-img-without-timestamps.zip` and once unzipped will have two files in the directory, `patchy_input.png` and `patchy_other.jpg`

###### Command
`curl -X POST 'http://localhost:7071/api/GrayscaleImages?include_timestamp=N' -F 'default_image_name=bar_image.png' -F 'images[0]=@./test_img/patchy_input.png' -F 'images[1]=@./test_img/patchy_other.jpg' -o output-zip-multi-img-without-timestamps.zip`

## Resources
- [Azure Create a Local Function Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser#create-a-local-function-project)
- [StackOverflow with Beneficial Information on Iterating over Multipart Files](https://stackoverflow.com/questions/55758899/azure-cloud-functions-http-file-upload-with-python)
- [StackOverflow that has different ways to us the PIL Image Python Library](https://stackoverflow.com/questions/61790607/how-do-i-receive-multipart-form-data-in-azure-function)
