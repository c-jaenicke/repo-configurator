# GitHub Repo Normalizer

## Requirements

Requires a GitHub Personal access tokens with the Repo scope enabled.

Can be made in: ``` GitHub -> Settings -> Developer settings -> Personal access tokens -> Generate new token```

Needs to be inserted in ```main.py``` in line 6 ```PAT_token = "TOKEN HERE"```


Python:
```
Python==3.9.7
requests==2.27.1
```

## How to

todo

## Available Changes to a Repo

[GitHub Documentation](https://docs.github.com/en/rest/reference/repos#update-a-repository)

| Name                   | Type               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                   | string             | The name of the repository.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| description            | string             | A short description of the repository.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| homepage               | string             | A URL with more information about the repository.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| private                | boolean            | Either true to make the repository private or false to make it public. Default: false.                                                                                                                                                                                                                                                                                                                                                                              |
| visibility             | string             | Can be public or private                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| security_and_analysis  | object or nullable | Specify which security and analysis features to enable or disable. For example, to enable GitHub Advanced Security, use this data in the body of the PATCH request: {"security_and_analysis": {"advanced_security": {"status": "enabled"}}}. If you have admin permissions for a private repository covered by an Advanced Security license, you can check which security and analysis features are currently enabled by using a GET /repos/{owner}/{repo} request. |
| has_issues             | boolean            | Either true to enable issues for this repository or false to disable them.                                                                                                                                                                                                                                                                                                                                                                                          |
| has_projects           | boolean            | Either true to enable projects for this repository or false to disable them. Note: If you're creating a repository in an organization that has disabled repository projects, the default is false, and if you pass true, the API returns an error.                                                                                                                                                                                                                  |
| has_wiki               | boolean            | Either true to enable the wiki for this repository or false to disable it.                                                                                                                                                                                                                                                                                                                                                                                          |
| is_template            | boolean            | Either true to make this repo available as a template repository or false to prevent it.                                                                                                                                                                                                                                                                                                                                                                            |
| default_branch         | string             | Updates the default branch for this repository.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| allow_squash_merge     | boolean            | Either true to allow squash-merging pull requests, or false to prevent squash-merging.                                                                                                                                                                                                                                                                                                                                                                              |
| allow_merge_commit     | boolean            | Either true to allow merging pull requests with a merge commit, or false to prevent merging pull requests with merge commits.                                                                                                                                                                                                                                                                                                                                       |
| allow_rebase_merge     | boolean            | Either true to allow rebase-merging pull requests, or false to prevent rebase-merging.                                                                                                                                                                                                                                                                                                                                                                              |
| allow_auto_merge       | boolean            | Either true to allow auto-merge on pull requests, or false to disallow auto-merge.                                                                                                                                                                                                                                                                                                                                                                                  |
| delete_branch_on_merge | boolean            | Either true to allow automatically deleting head branches when pull requests are merged, or false to prevent automatic deletion.                                                                                                                                                                                                                                                                                                                                    |
| archived               | boolean            | true to archive this repository. Note: You cannot unarchive repositories through the API.                                                                                                                                                                                                                                                                                                                                                                           |
| allow_forking          | boolean            | Either true to allow private forks, or false to prevent private forks.                                                                                                                                                                                                                                                                                                                                                                                              |

### Example changes.json

```
{
    "name": "a cool repo",
    "description": "some text",
    "homepage": null,
    "private": true,
    "visibility": "private",
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true,
    "is_template": false,
    "default_branch": "main",
    "allow_squash_merge": true,
    "allow_merge_commit": true,
    "allow_rebase_merge": true,
    "allow_auto_merge": false,
    "delete_branch_on_merge": false,
    "archived": false,
    "allow_forking": true
}
```