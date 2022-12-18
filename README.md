# bbarchive

## Introduction
The `bbarchive` tool let you archive all existing repositories from a source project to another destination project.

## Requirements
This tool requires Python version 3.7 or newer.

## Too long; didn't read

Update the `init.sh` file
- update `BITBUCKET_URL`
- update `BITBUCKET_USERNAME`
- update `BITBUCKET_PASSWORD`

Source the `init.sh` file
```shell
source init.sh
```

To migrate all repositories from Bitbucket project AAA to project BBB, run:

```shell
python bbarchive.py -s AAA -d BBB --overwrite
```

## Help
To show the full help message, run `python bbarchive.py -h`

```shell
usage: bbarchive.py [-h] [--dry-run] -s SOURCE_KEY -d DESTINATION_KEY
                    [--overwrite] [--name-prefix NAME_PREFIX]
                    [--description-prefix DESCRIPTION_PREFIX] [--debug]
                    [--warning]

Create an Archive BitBucket Project

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             Enable dry-run (defaults to "false")
  -s SOURCE_KEY, --source SOURCE_KEY
                        (required) Source Bitbucket project key
  -d DESTINATION_KEY, --destination DESTINATION_KEY
                        (required) Destination Bitbucket project key
  --overwrite           Continue if Bitbucket source project already exists
  --name-prefix NAME_PREFIX
                        String to prefix at the beginning of the project's
                        name (defaults to "(Archived) ")
  --description-prefix DESCRIPTION_PREFIX
                        Character(s) to append to the end of the project's
                        description (defaults to "(Archived) ")
  --debug               Display "debugging" in output (defaults to "info")
  --warning             Display "warning" in output only (no "info" messages)
 ```

## FAQ 

**Q:**
How come I'm getting the following error:

```
ERROR:root:Terminating because destination Bitbucket project "AAA" exists. To continue, re-run with the "--overwrite" parameter present```
```

**A:**
The destination project `BBB` already exists. If you are ok (e.g. reusing the `BBB` project), re-run with the `--overwrite` parameter

```shell
python bbarchive.py -s AAA -d BBB --overwrite
```

##
**Q:**
How do I increase logging level (e.g. "debug" mode)?

**A:**
Append the argument `--verbose`.

##
**Q:**
How do I silent "INFO" level messages?

**A:**
Append the argument `--warning`. The application will only output `WARNING` and `ERROR` messages only/


