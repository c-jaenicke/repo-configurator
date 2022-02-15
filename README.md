# GitHub Repo Normalizer

## Requirements

Requires a GitHub Personal access tokens with the Repo scope enabled.

Can be made in: ` GitHub -> Settings -> Developer settings -> Personal access tokens -> Generate new token`

Needs to be inserted in `main.py` in line 6 `PAT_token = "TOKEN HERE"`

Python:

```
Python==3.9.7

certifi==2021.10.8
charset-normalizer==2.0.11
idna==3.3
requests==2.27.1
urllib3==1.26.8
wincertstore==0.2
```

## How to

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

## Available Options when Creating a Repo

[GitHub Documentation](https://docs.github.com/en/rest/reference/repos#create-a-repository-for-the-authenticated-user)

| Name                   | Type    | Description                                                                                                                          |
| ---------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| name                   | string  | Required. The name of the repository.                                                                                                |
| description            | string  | A short description of the repository.                                                                                               |
| homepage               | string  | A URL with more information about the repository.                                                                                    |
| private                | boolean | Whether the repository is private. _Default: false_                                                                                  |
| has_issues             | boolean | Whether issues are enabled. _Default: true_                                                                                          |
| has_projects           | boolean | Whether projects are enabled. _Default: true_                                                                                        |
| has_wiki               | boolean | Whether the wiki is enabled. _Default: true_                                                                                         |
| team_id                | integer | The id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization. |
| auto_init              | boolean | Whether the repository is initialized with a minimal README. _Default: false_                                                        |
| gitignore_template     | string  | The desired language or platform to apply to the .gitignore.                                                                         |
| license_template       | string  | The license keyword of the open source license for this repository.                                                                  |
| allow_squash_merge     | boolean | Whether to allow squash merges for pull requests. _Default: true_                                                                    |
| allow_merge_commit     | boolean | Whether to allow merge commits for pull requests. _Default: true_                                                                    |
| allow_rebase_merge     | boolean | Whether to allow rebase merges for pull requests. _Default: true_                                                                    |
| allow_auto_merge       | boolean | Whether to allow Auto-merge to be used on pull requests. _Default: false_                                                            |
| delete_branch_on_merge | boolean | Whether to delete head branches when pull requests are merged. _Default: false_                                                      |
| has_downloads          | boolean | Whether downloads are enabled. _Default: true_                                                                                       |
| is_template            | boolean | Whether this repository acts as a template that can be used to generate new repositories. _Default: false_                           |

### Example changes.json

```
{
    "name": "a new repo i created",
    "description": "this repo does a thing",
    "homepage": null,
    "private": false,
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true,
    "team_id": null,
    "auto_init": false,
    "gitignore_template": null,
    "license_template": null,
    "allow_squash_merge": true,
    "allow_merge_commit": true,
    "allow_rebase_merge": true,
    "allow_auto_merge": false,
    "delete_branch_on_merge": false,
    "has_downloads": true,
    "is_template": false
}