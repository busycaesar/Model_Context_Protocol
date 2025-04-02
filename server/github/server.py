import os
from mcp.server.fastmcp import FastMCP
from github import Github

mcp = FastMCP("github")

class GitHub:
    def __init__(self, access_token):
        self.github = Github(access_token)
        self.user = self.github.get_user()
        self.username = self.user.login
        
    def create_new_repo(self, name, description = "", private = False):
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private
            )

            readme_content = f"# {name}"

            repo.create_file("README.md", "Add README.md", readme_content)
        except Exception as e:
            raise ValueError(f"Failed to create repository: {e}")

    def _get_repository(self, repo_name):
        try:
            return self.github.get_repo(f"{self.username}/{repo_name}")
        except Exception as e:
            raise ValueError(f"Failed to get repository: {e}")

    def list_branches(self, repo_name):
        repo = self._get_repository(repo_name)

        try:
            branches = repo.get_branches()
            return [branch.name for branch in branches]
        except Exception as e:
            raise ValueError(f"Failed to list branches: {e}")

    def create_branch(self, repo_name, base_branch, new_branch_name):
        repo = self._get_repository(repo_name)

        try:
            base_commit = repo.get_branch(base_branch).commit
            repo.create_git_ref(
                ref=f"refs/heads/{new_branch_name}",
                sha=base_commit.sha
            )
        except Exception as e:
            raise ValueError(f"Failed to create the new branch: {e}")

    def delete_branch(self, repo_name, branch_name):
        repo = self._get_repository(repo_name)
        
        try:
            ref = repo.get_git_ref(f"heads/{branch_name}")

            ref.delete()
        except Exception as e:
            raise ValueError(f"Failed to delete the branch: ${e}")

    def create_issue(self, repo_name, issue_title, issue_description):
        repo = self._get_repository(repo_name)

        try:
            repo.create_issue(
                title=issue_title,
                body=issue_description
            )
        except Exception as e:
            raise ValueError(f"Failed to delete the branch: ${e}")

GH_ACCESS_TOKEN = os.getenv("GH_ACCESS_TOKEN")

if not GH_ACCESS_TOKEN:
    raise ValueError("Please set the GH_ACCESS_TOKEN environment variable to github's access token.")

github = GitHub(GH_ACCESS_TOKEN)

@mcp.tool()
def create_new_repo(name, description, private):
    """
    Create a new repository on the GitHub.

    Args:
        name: The name of the new github repo to be created.
        description: The description for the github repo.
        private: A bool value to indicate if the repo should be private or public.
    """
    try:
        github.create_new_repo(name, description, private)
    except Exception as e:
        raise ValueError(e)
    
@mcp.tool()
def list_branches(repo_name):
    """
    List all the branches in the repository.
    
    Args:
        repo_name: The desired name of the new repositry.
    """
    try:
        github.list_branches(repo_name)
    except Exception as e:
        raise ValueError(e)

@mcp.tool()
def create_branch(repo_name, base_branch, new_branch_name):
    """
    Create a new branch in the existing github repo.
    
    Args:
        repo_name: Name of the existing repo in which the branch is to be created.
        base_branch: The branch from which the new branch is to be created.
        new_branch_name: The desired name for the new branch.
    """
    try:
        github.create_branch(repo_name, base_branch, new_branch_name)
    except Exception as e:
        raise ValueError(e)

@mcp.tool()
def delete_branch(repo_name, branch_name):
    """
    Delete an existing branch from the existing github repository.
    
    Args:
        repo_name: The name of the existing github repository. 
        branch_name: The name of the existing branch to be deleted.
    """
    try:
        github.delete_branch(repo_name, branch_name)
    except Exception as e:
        raise ValueError(e)

@mcp.tool()
def create_issue(repo_name, issue_title, issue_description):
    """
    Create a new issue in the github repository.
    
    Args:
        repo_name: Name of the existing github repository.
        issue_title: Title for the new issue.
        issue_description: Description for the new issue.
    """
    try:
        github.create_issue(repo_name, issue_title, issue_description)
    except Exception as e:
        raise ValueError(e)

if __name__ == "__main__":
    # Initialize and run the server.
    mcp.run(transport='stdio')