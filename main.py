import json
import requests
import argparse

# SET YOUR PERSONAL ACCESS TOKEN HERE
PAT_token = "TOKEN HERE"

def make_request(endpoint):
    '''DONT USE
    only here for future reference'''
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


def request_repo_info(repo):
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


def request_repo_change(repo, changeFile):
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
    if "." in repo:
        file = open(repo)
        for line in file:
            line = line.strip("\n")
            responseJson = request_repo_info(line)
            if args.json:
                write_info_to_file(line, responseJson)
            if args.view:
                print_repo_info(line, responseJson)
        
    else: 
        responseJson = request_repo_info(repo)
        if args.json:
                write_info_to_file(repo, responseJson)
        if args.view:
            print_repo_info(repo, responseJson)


def make_changes(repo):
    if "." in repo:
        file = open(repo)
        for line in file:
            line = line.strip("\n")
            responseJson = request_repo_change(line, args.changes)
            if args.json:
                write_info_to_file(line + "--changed", responseJson)
            if args.view:
                print_repo_info(line, responseJson)
    
    else: 
        responseJson = request_repo_change(repo, args.changes)
        if args.json:
                write_info_to_file(repo + "--changed", responseJson)
        if args.view:
            print_repo_info(repo, responseJson)


#def main():
#   return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="GitHub Repo Normalizer" ,description="Normalize GitHub repo settings")
    parser.add_argument("-op",
                        choices=["getinfo", "changerepo"],
                        default="getinfo",
                        help="Specify what operation should done")

    parser.add_argument("-repo", type=str,
                        default="repos.txt",
                        help="provide the name of a file containing a list of repos, each in a new line")

    parser.add_argument("-json",
                        default=False,
                        action="store_true",
                        help="When used the info about a repo will be saved in a .json")

    parser.add_argument("-view",
                        default=False,
                        action="store_true",
                        help="When used the info about a repo will be printed into the console")

    parser.add_argument("-changes", type=str,
                        default="changes.json",
                        help="file containing the changes to be made to the repo in a JSON format. Default is changes.json. Please use https://jsonformatter.curiousconcept.com/ for testing your JSON")

    args = parser.parse_args()

    if args.op == "getinfo":
        collect_info(args.repo)

    elif args.op == "changerepo":
        make_changes(args.repo)

