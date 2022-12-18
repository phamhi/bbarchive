from pprint import pprint, pformat
from f import *
import sys

# ----------------------------------------------------------------------------------------------------------------------

str_env_url = 'BITBUCKET_URL'
str_env_username = 'BITBUCKET_USERNAME'
str_env_password = 'BITBUCKET_PASSWORD'

# Postfix strings to be added to the Archive Project.
str_archive_project_name_prefix = '(Archived) '
str_archive_project_description_prefix = '(Archived) '
str_api_projects = '/rest/api/latest/projects'

dict_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # parse arguments passed
    args = parse_args(str_archive_project_name_prefix, str_archive_project_description_prefix)

    # copy args to local variables (easier to refactor in IDE)
    str_source_key = args.source_key
    str_destination_key = args.destination_key
    int_verbosity = args.verbosity
    str_name_prefix = args.name_prefix
    str_description_prefix = args.description_prefix
    bool_overwrite = args.overwrite
    bool_dry_run = args.dry_run

    # set logging verbosity
    logging.basicConfig(level=args.verbosity)

    # output running mode
    logging.info(f'Mode "dry-run" (show action plans only): "{args.dry_run}"')
    logging.info(f'Mode "overwrite" (continue if source Bitbucket project exists): "{args.overwrite}"')
    logging.info(f'Verbosity "level": "{logging.getLevelName(args.verbosity)}"')

    # retrieve environment variables
    str_url, str_username, str_password = get_env(str_env_url, str_env_username, str_env_password)

    # ensure pre-req environment variables are set
    if not str_url:
        logging.error(f'Environment variable "{str_env_url}" is not set')
        sys.exit(1)
    # /if
    if not str_username:
        logging.error(f'Environment variable "{str_env_username}" is not set')
        sys.exit(2)
    # /if
    if not str_password:
        logging.error(f'Environment variable "{str_env_password}" is not set')
        sys.exit(3)
    # /if

    # output processed environment variables
    logging.info(f'{str_env_url}: "{str_url}"')
    logging.info(f'{str_env_username}: "{str_username}"')
    logging.info(f'{str_env_password}: "{(str_password[:1]) + len(str_password[1:-1]) * "*" + str_password[-1:]}"')

    logging.info(f'Source Bitbucket project: "{str_source_key}"')
    logging.info(f'Destination Bitbucket project: "{str_destination_key}"')

    # establish bitbucket connection
    bitbucket = get_bitbucket(str_url, str_username, str_password)
    try:
        dict_source = bitbucket.project(str_source_key)
    except Exception as e:
        logging.error(f'Cannot connect to server "{str_url}":\n> {e}')
        if int_verbosity <= logging.DEBUG:
            raise
        # /if
        sys.exit(4)
    # /except
    logging.info(f'Successfully connected to Bitbucket server: "{str_url}"')

    # process source project
    logging.info(f'Bitbucket source project "{str_source_key}" information:\n'
                 f'{pformat(dict_source)}')
    # get list of repository
    list_source_repos = [repo['name'] for repo in bitbucket.repo_list(str_source_key)]
    if not list_source_repos:
        logging.warning(f'Bitbucket source project "{str_source_key}" has no repositories. Terminating...')
        sys.exit(0)
    # /if

    logging.info('Getting existing Bitbucket project keys...')
    list_dict_projects = [project for project in bitbucket.project_list()]

    list_str_keys = [i['key'] for i in list_dict_projects]
    logging.debug(f'Existing Bitbucket project keys: {list_str_keys}')

    # create definition for destination project
    dict_destination = {
        'key': f'{str_destination_key}',
        'name': f'{str_name_prefix}{dict_source["name"]}',
        'description': f'{str_description_prefix}{dict_source["description"]}'
    }
    logging.info(f'Destination Bitbucket project information:\n'
                 f'{pformat(dict_destination)}')

    # check if destination project key already exists
    bool_exists = dict_destination['key'] in list_str_keys
    if bool_exists:
        logging.warning(f'Bitbucket project with the key "{str_destination_key}" already exists')
    # /if

    # destination project key exists but "--overwrite" argument wasn't passed
    if bool_exists and not bool_overwrite:
        logging.error(f'Terminating because destination Bitbucket project "{str_destination_key}" exists. '
                      f'To continue, re-run with the "--overwrite" parameter present')
        sys.exit(5)
    # /else

    # destination project key doesn't exist; will try to create a new project
    if not bool_exists:
        logging.info(f'Creating new destination Bitbucket project: "{str_destination_key}"')

        if not bool_dry_run:
            bitbucket.create_project(
                dict_destination['key'],
                dict_destination['name'],
                description=dict_destination['description'],
            )
        # /if
    # /if

    logging.info(f'List of git repositories found in Bitbucket source project "{str_source_key}":\n'
                 f'{pformat(list_source_repos)}')

    list_destination_repos = [repo['name'] for repo in bitbucket.repo_list(str_destination_key)]

    if list_destination_repos:
        logging.info(f'List of git repositories found in Bitbucket destination project "{str_destination_key}":\n'
                     f'{pformat(list_destination_repos)}')
    # /if

    # remove duplicate repositories
    list_migrate_repos = list(set(list_source_repos) - set(list_destination_repos))

    # is the migration list empty?
    if list_destination_repos:
        logging.info(f'There are no repositories that can be migrated')
    else:
        logging.info(f'The following git repositories will be migrated from project "{str_source_key}" to "{str_destination_key}":\n'
                     f'{pformat(list_migrate_repos)}')
    # /if

    # move repositories
    if not bool_dry_run:
        for str_repo_name in list_migrate_repos:
            dict_result = bitbucket.update_repo(str_source_key, str_repo_name, project=dict(key=str_destination_key))
            str_key_verification = dict_result.setdefault('project', {'key': ''}).setdefault('key', '')

            if str_key_verification == str_destination_key:
                logging.info(f'Successfully migrated repo: "{str_repo_name}"')
            else:
                logging.warning(f'Failed migrated repo: "{str_repo_name}"')
            # /if
        # /for
    # /if

    logging.info(f'Exiting')


# /if main
