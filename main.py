import json
import requests
import argparse
from datetime import date
import sys

# SET YOUR PERSONAL ACCESS TOKEN HERE
PAT_token = "TOKEN HERE"


def repo_requests(operation: str, repo: str, fileName=""):
    ApiUrlBase = "https://api.github.com/repos"
    ApiUrl = "{0}/{1}".format(ApiUrlBase, repo)
    headers = { "Content-Type": "application/json",
                "Authorization": "token {0}".format(PAT_token)
    }

    if operation == "get":
        return requests.get(ApiUrl, headers=headers)

    elif operation == "patch":
        changesJson = read_file(fileName)
        return requests.patch(ApiUrl, data=changesJson, headers=headers)

    elif operation == "post":
        url = "https://api.github.com/user/repos"
        repoSettings = str(read_file(fileName))
        return requests.post(ApiUrl, data=repoSettings, headers=headers)

    else:
        print("Invalid operation specified - Exit(0)")
        sys.exit(1)


def gist_requests(operation: str, repo: str, fileName=""):
    ApiUrlBase = "https://api.github.com/gists"
    headers = { "Accept":"application/vnd.github.v3+json",
                "Authorization":"token {0}".format(PAT_token)
    }

    def post_gist(url: str, headers: dict, fileName: str, repo: str):
        content ={"description": "description",
                "public": False,
                "files": { 
                    "RepoInfo": {
                        "content": "fileContent"
                    }
                }
        }
        description = "Info for repo {0}".format(repo)
        gistContent = read_file(fileName)
        gistName = "RepoInfo--{0}--{1}".format(date.today().isoformat(), fileName)
        content["description"] = description
        content["files"] = {gistName: {"content": str(gistContent)}}
        content = json.dumps(content,sort_keys=False, indent=4)
        return requests.post(ApiUrlBase, data=content, headers=headers)

    def get_gist():
        # TODO
        return

    if operation == "post":
        response = post_gist(ApiUrlBase, headers, fileName, repo)

    elif operation == "post":
        response = get_gist()
        
    else:
        print("Invalid operation specified - Exit(0)")
        sys.exit(1)

    return process_response(response, repo)


def process_response(response, repo: str):
    if response.status_code == 200:
        print("200 - Successful request for repo {0}".format(repo))
        responseJson = json.loads(response.content.decode("utf-8"))
        return responseJson

    elif response.status_code == 201:  
        responseJson = json.loads(response.content.decode("utf-8"))
        print("201 - Successfully created - {0}".format(responseJson["html_url"]))
        return responseJson

    elif response.status_code == 422:  
        responseJson = json.loads(response.content.decode("utf-8"))
        print("422 - Unprocessable Entity for repo {0}\n\tError: {1}\n\tIt probably still worked, please check!".format(repo, responseJson))
        return responseJson

    else:
        print("{0} - Failed request for repo {1}".format(response.status_code, repo))
        responseJson = json.loads(response.content.decode("utf-8"))
        print(responseJson)
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


def write_file(repoName, responseJson):
    '''write pretty json data to a file

    Args:
        repoName: name of the repo
        responseJson: json data returned by request_info/change_repo functions'''
    repoName = repoName.replace("/","-")
    fileName = (repoName + ".json")
    file = open(fileName, "w")
    file.write(json.dumps(responseJson, sort_keys=False, indent=4))
    file.close()
    return fileName


def read_file(fileName):
    '''reads file that contains the json formatted changes and returns them as a string

    Args:
        changeFile: name of the file that contains the values
        
    Returns:
        changesJson: string in json format'''
    file = open(fileName,"r")
    changesJson = file.read()
    return changesJson


def get_repo_info(repo):
    if "." in repo:
        file = open(repo)
        for line in file:
            line = line.strip("\n")
            responseJson = repo_requests("get", line)
            if args.json:
                write_file(line, responseJson)
            if args.view:
                print_repo_info(line, responseJson)
            if args.gist:
                fileName = write_file(line, responseJson)
                gist_requests("post", line, fileName)
        
    else: 
        responseJson = get_repo_info(repo)
        if args.json:
            write_file(repo, responseJson)
        if args.view:
            print_repo_info(repo, responseJson)
        if args.gist:
            fileName = write_file(repo, responseJson)
            gist_requests("post", repo, fileName)


def make_changes(repo):
    if "." in repo:
        file = open(repo)
        for line in file:
            line = line.strip("\n")
            responseJson = repo_requests("patch",line, args.changes)
            if args.json:
                write_file(line + "--changed", responseJson)
            if args.view:
                print_repo_info(line, responseJson)
    
    else: 
        responseJson = repo_requests("patch", repo, args.changes)
        if args.json:
            write_file(repo + "--changed", responseJson)
        if args.view:
            print_repo_info(repo, responseJson)


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
            -gist ; default = false ; when used the info about a repo will be uploaded in a private gist

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

    parser.add_argument("-gist",
                        default=False,
                        action="store_true",
                        help="Default = False ;  When used the info about a repo will be uploaded in a private gist.")

    args = parser.parse_args()

    if args.op == "getinfo":
        get_repo_info(args.repo)

    elif args.op == "changerepo":
        # because changes can be disruptive, an extra step
        confirm = input("CONFIRM THAT YOU WANT TO MAKE THESE CHANGES! y/n ")
        if confirm == "y" or confirm == "Y":
            make_changes(args.repo)
        else:
            print("Stopping ...")

    elif args.op == "createrepo":
        repo_requests("post","",args.changes)

    # triggers when no op is specified
    else:
        print("No valid operation entered, please use -h for help.")