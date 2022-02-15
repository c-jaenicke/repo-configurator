import json
from weakref import ref
import requests
import argparse

# SET YOUR PERSONAL ACCESS TOKEN HERE
PAT_token = "TOKEN HERE"

def make_request(endpoint):
    '''DONT USE
    only here for future reference and testing'''
    ApiUrlBase = "https://api.github.com/"
    ApiUrl = "{0}{1}".format(ApiUrlBase, endpoint)

    headers = { "Content-Type": "application/json",
                "Authorization": "token {0}".format(PAT_token),
    }

    print(ApiUrl)
    response = requests.get(ApiUrl, headers=headers)

    if response.status_code == 200:
        print("--- Successful")
        responseJson = json.loads(response.content.decode("utf-8"))
        #print(responseJson)
        return responseJson
    else:
        print("--- Failed")
        print(str(response.status_code))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson


def get_repo_info(repo):
    '''request info of a repo

    Args:
        repo: owner/name to a repo

    Returns:
        responseJson: json containing data or the cause of error'''
    ApiUrlBase = "https://api.github.com/repos/"
    ApiUrl = "{0}{1}".format(ApiUrlBase, repo)
    headers = { "Content-Type": "application/json",
                "Authorization": "token {0}".format(PAT_token),
    }
    response = requests.get(ApiUrl, headers=headers)

    if response.status_code == 200:
        print("--- Successful info request 200 for repo {0} ---".format(repo))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson
    else:
        print("--- Failed info request {0} for repo {1} ---".format(response.status_code, repo))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson


def patch_repo_change(repo, changeFile):
    '''request change of a repo

    Args:
        repo: owner/name to a repo
        changeFile: file containing values to change in a json format

    Returns:
        responseJson: json containing data or the cause of error'''
    ApiUrlBase = "https://api.github.com/repos/"
    ApiUrl = "{0}{1}".format(ApiUrlBase, repo)
    headers = { "Content-Type": "application/json",
                "Authorization": "token {0}".format(PAT_token)
    }
    # read changes to be made from json file
    changesJson = read_changes_from_file(changeFile)
    response = requests.patch(ApiUrl, data=changesJson, headers=headers, )

    if response.status_code == 200:
        print("--- Successful repo change 200 for repo {0} ---".format(repo))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson
    else:
        print("--- Failed repo change {0} for repo {1} ---".format(response.status_code, repo))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson


def post_create_repo(changeFile):
    '''create a repo with defined values

    Args:
        changeFile: file containing values in json format

    Returns:
        responseJson: json containing data or the cause of error'''
    ApiUrlBase = "https://api.github.com/user/repos"

    headers = { "Content-Type": "application/json",
                "Authorization": "token {0}".format(PAT_token)
    }
    # read new repo settings from file
    changesJson = read_changes_from_file(changeFile)
    response = requests.post(ApiUrlBase, data=changesJson, headers=headers, )

    if response.status_code == 200 or response.status_code == 201:
        print("--- Successful created repo 200 ---")
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson
    else:
        print("--- Failed repo creation {0} ---".format(response.status_code))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson


def print_repo_info(repo, data):
    '''print the info of a repo in the console
    
    Args:
        repo: name of the repo
        data: json data returned by request_info/change_repo functions'''
    print("""Info about repo {0}
    Owner: {1} 
    Visibility: {2}
    URL: {3}
    Name: {4}
    Description: {5}
    
    List of Features
        Issues enabled: {6}
        Projects enabled: {7}
        Downloads enabled: {8}
        Wiki enabled: {9}
        Pages enabled: {10}

    Stats:
        Forks: {11}
        Open issues: {12}
        Watchers: {13}
        Subscribers: {14}"""
    .format( 
    repo, # 0
    data["owner"]["login"], # 1
    data["visibility"], # 2
    data["html_url"], # 3
    data["name"], # 4
    data["description"], # 5
    data["has_issues"], # 6
    data["has_projects"], # 7
    data["has_downloads"], # 8
    data["has_wiki"], # 9
    data["has_pages"], # 10
    data["forks"], # 11
    data["open_issues"], # 12
    data["watchers"], # 13
    data["subscribers_count"], # 14
    ))


def write_info_to_file(repoName, responseJson):
    '''write pretty json data to a file

    Args:
        repoName: name of the repo
        responseJson: json data returned by request_info/change_repo functions'''
    repoName = repoName.replace("/","-")
    file = open(repoName + ".json", "w")
    file.write(json.dumps(responseJson, sort_keys=False, indent=4))
    file.close()


def read_changes_from_file(changeFile):
    '''reads file that contains the json formatted changes and returns them as a string

    Args:
        changeFile: name of the file that contains the values
        
    Returns:
        changesJson: string in json format'''
    file = open(changeFile,"r")
    changesJson = file.read()
    return changesJson


def collect_info(repo):
    '''connector for reading info to repos'''
    if "." in repo:
        file = open(repo)
        for line in file:
            line = line.strip("\n")
            responseJson = get_repo_info(line)
            if args.json:
                write_info_to_file(line, responseJson)
            if args.view:
                print_repo_info(line, responseJson)
        
    else: 
        responseJson = get_repo_info(repo)
        if args.json:
                write_info_to_file(repo, responseJson)
        if args.view:
            print_repo_info(repo, responseJson)


def make_changes(repo):
    '''connector for making changes to repos'''
    if "." in repo:
        file = open(repo)
        for line in file:
            line = line.strip("\n")
            responseJson = patch_repo_change(line, args.changes)
            if args.json:
                write_info_to_file(line + "--changed", responseJson)
            if args.view:
                print_repo_info(line, responseJson)
    
    else: 
        responseJson = patch_repo_change(repo, args.changes)
        if args.json:
                write_info_to_file(repo + "--changed", responseJson)
        if args.view:
            print_repo_info(repo, responseJson)

# NOTE collect_info and make_changes can be put together in the future as parse_repo or something


if __name__ == "__main__":
    # build parser
    parser = argparse.ArgumentParser(prog="GitHub Repo Normalizer" ,description="Normalize GitHub repo settings", formatter_class=argparse.RawTextHelpFormatter)

    # string to be displayed for operation help
    help_string = """Sets operation to be performed:
    getinfo: returns info on the given repo, e.g. if its private and number of issues
        Args: 
            -repo <value> ; default = repos.txt ; takes a file to be iterated through or a single repo
                repo needs to be formatted as "owner/repo_name", e.g. "c-jaenicke/repo_configurator"
            -view ; default = false ; displays info about the repo in the terminal
            -json ; default = false ; prints the info about the repo in a json file

    changerepo: changes the settings of a repo
        Args:
            -repo <value> ; default = repos.txt ; takes a file to be iterated through or a single repo
                repo needs to be formatted as "owner/repo_name", e.g. "c-jaenicke/repo_configurator"
            -changes <value> ; default = changes.json ; specifies the file that will be read, which contains the changes to be made, see README.md for possible values

    createrepo: creates a repo with the specified settings
        Args:
            -changes <value> ; default = changes.json ; specifies which settings the new repo will have, see README.md for possible values
    """

    parser.add_argument("op",
                        choices=["getinfo", "changerepo", "createrepo"],
                        help=help_string)

    parser.add_argument("-repo", type=str,
                        default="repos.txt",
                        help="Default = repos.txt ; Reads a specified file for a list of repos, or takes a single repo, the names need to be formatted as \"owner/repo_name\" e.g. c-jaenicke/repo_configurator .")

    parser.add_argument("-json",
                        default=False,
                        action="store_true",
                        help="Default = False ;  When used the info about a repo will be stored in a .json file.")

    parser.add_argument("-view",
                        default=False,
                        action="store_true",
                        help="Default = False ;  When used the info about a repo will be displayed in the terminal.")

    parser.add_argument("-changes", type=str,
                        default="changes.json",
                        help="Default = changes.json ; Reads a specified file for changes to be made in a json format. Please use https://jsonformatter.curiousconcept.com/ for testing your JSON. Possible values are in the README.md.")

    args = parser.parse_args()

    if args.op == "getinfo":
        collect_info(args.repo)

    elif args.op == "changerepo":
        # because changes can be disruptive, an extra step
        confirm = input("--- CONFIRM THAT YOU WANT TO MAKE THESE CHANGES! y/n ---")
        if confirm == "y" or confirm == "Y":
            make_changes(args.repo)
        else:
            print("--- Stopping ... ---")

    elif args.op == "createrepo":
        post_create_repo(args.changes)

    # triggers when no op is specified
    else:
        print("No valid operation entered, please use -h for help.")

